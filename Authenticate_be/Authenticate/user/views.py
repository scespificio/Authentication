import json

from django.shortcuts import render
from django.conf import settings
from urllib.parse import urlparse
from django.template.loader import render_to_string
from rest_framework.status import HTTP_400_BAD_REQUEST

from django.shortcuts import redirect

from rest_framework import permissions, status
from rest_framework.generics  import GenericAPIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator

from django.http import FileResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.cache import cache
from .serializers import CustomTokenObtainPairSerializer
from djoser.serializers import ActivationSerializer as DJActivationSerializer, SendEmailResetSerializer
from django_clamd.validators import validate_file_infection
import logging
logger = logging.getLogger(__name__)

from rest_framework_simplejwt.views import TokenObtainPairView
from .tasks import send_email
from django.contrib import messages
from django.contrib.auth import get_user_model
from djoser.utils import decode_uid
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
#from user.services.activation import send_activation_email
from user.emails import ActivationEmail, PasswordResetEmail
from urllib.parse import urljoin
import djoser, inspect
import os
import datetime as dt
from dotenv import load_dotenv

load_dotenv()

CONFIG_FOLDER = os.getenv('CONFIG_FILE_FOLDER')
CONFIG_FILE = os.getenv('CONFIG_FILE_NAME')

@api_view(["GET"])
def home(request):
    return Response({"message": "Hello, world. You're at the home page."})

class ConfigDetailView(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    #serializer_class = WebConfigOutputSerializer
    # pas de listing; on garde select_related pour éviter les N+1
    #queryset = WebConfig.objects.select_related("emailTemplate", "ui_template").none()

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        file_path = os.path.join(settings.BASE_DIR, CONFIG_FOLDER, CONFIG_FILE)

        if not os.path.exists(file_path):
            return Response(
                {"error":f"JSON file not found at:{file_path}"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return Response(data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


User = get_user_model()
def get_user_from_uid_token(uid: str, token: str):
    """
    Retourne (user, is_valid)
    - user : instance User ou None
    - is_valid : True si le token correspond et n'est pas expiré
    """

    if not uid or not token:
        return None, False

    try:
        user_id = decode_uid(uid)
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None, False

    # Vérifie la validité du token
    is_valid = default_token_generator.check_token(user, token)
    return user, is_valid

class ActivationView(APIView):
    permission_classes = [AllowAny]  # l’activation est anonyme
    token_generator = default_token_generator  # <<< important


    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        user, is_valid = get_user_from_uid_token(uid, token)
        
        if not request.data.get("uid") or not request.data.get("token"):
            email = request.data.get("email")
            user = User.objects.filter(email=email).first()

            if not user:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            if user.is_active:
                return Response({"detail": "Compte déjà activé"}, status=status.HTTP_403_FORBIDDEN)
            s = SendEmailResetSerializer(data={"email": email}, context={"request": request}) 
        
        s = DJActivationSerializer(data={"uid": uid, "token": token}, context={"request": request, "view": self})   
        s.is_valid(raise_exception=True)
        user.is_active = True
        user.save(update_fields=["is_active"])

        if not cache.add(f"password:reset-sent:view:{user.pk}", "1", timeout=60*1):
            logger.info("[password] skip duplicate (view) for %s", user.email)
        else:
            token = default_token_generator.make_token(user)
            # Contexte attendu par ta classe ActivationEmail
            ctx = {
                "user": user,
                "uid": uid,
                "token": token,
                # Djoser fournit normalement url via ACTIVATION_URL,
                # mais si tu veux, construis-la côté front à partir de ces deux valeurs.
                "frontend_url": settings.FRONTEND_BASE_URL,
                "site_name": getattr(settings, "EMAIL_FRONTEND_SITE_NAME", None) or "Site",
                "domain": settings.DJOSER.get("DOMAIN", ""),
                "request": request,
            }
            print("Activation view ctx:", ctx)
            PasswordResetEmail(context=ctx).send(to=user.email)

        return Response(
            {"detail": "Activation réussie."},
            status=status.HTTP_200_OK,
        )

class ActivationResendView(APIView):
    permission_classes = [AllowAny]  # l’activation est anonyme
    
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email requis."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Aucun utilisateur trouvé avec cet email."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.is_active:
            return Response(
                {"detail": "Compte déjà activé."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Contexte attendu par ta classe ActivationEmail
        ctx = {
            "user": user,
            "uid": uid,
            "token": token,
            # Djoser fournit normalement url via ACTIVATION_URL,
            # mais si tu veux, construis-la côté front à partir de ces deux valeurs.
            "activation_url": urljoin(settings.FRONTEND_BASE_URL, f"/activate/{uid}/{token}"),
            "site_name": getattr(settings, "EMAIL_FRONTEND_SITE_NAME", None) or "Site",
            "domain": request.get_host(),
            "request": request,
        }
        ActivationEmail(context=ctx).send(to=user.email)
        return Response(
            {"detail": "Lien d'activation réinitialisé."},
            status=status.HTTP_204_NO_CONTENT,
        )


    