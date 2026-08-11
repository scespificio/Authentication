from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError

from .models import ProfilUtilisateur, Domaine
from .serializers import ProfileSerializer, DomainSerializer, CoreTokenObtainPairSerializer
from users.serializers import CustomTokenObtainPairSerializer
from users.models import User
from .services import user_has_domain_access

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics  import GenericAPIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import NotAuthenticated

from dotenv import load_dotenv
import os
import json

load_dotenv()

CONFIG_FOLDER = os.getenv('CONFIG_FILE_FOLDER')
CONFIG_FILE = os.getenv('CONFIG_FILE_NAME')

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

class ProfileView(GenericAPIView): # GET all
    serializer_class = ProfileSerializer
    queryset = ProfilUtilisateur.objects.all()

    def get(self, request):
        obj = self.get_queryset()
        return Response(self.get_serializer(obj, many=True).data, status=status.HTTP_200_OK)

class ProfileViewDetail(GenericAPIView): # GET one
    serializer_class = ProfileSerializer
    queryset = ProfilUtilisateur.objects.all()

    def get(self, request):
        obj = self.get_queryset().filter(utilisateur=request.user)
        return Response(self.get_serializer(obj, many=True).data, status=status.HTTP_200_OK)

class DomainView(GenericAPIView): # GET all (TEMPORAIRE)
    serializer_class = DomainSerializer
    queryset = Domaine.objects.all()

    def get(self, request):
        obj = self.get_queryset()
        return Response(self.get_serializer(obj, many=True).data, status=status.HTTP_200_OK)

class DomainUserView (GenericAPIView): # GET all domaines associés avec l'utilisateur
    serializer_class = DomainSerializer
    queryset = Domaine.objects.all()

    def get(self, request):
        obj = self.get_queryset().filter(profils__utilisateur=request.user)
        return Response(self.get_serializer(obj, many=True).data, status=status.HTTP_200_OK)

class AuthorizeView(GenericAPIView):# GET response
    def get(self, request):

        if not "X-Requested-Host" in request.headers: # Aucun paramètre = tentative de connexion à la page d'accueil.
            is_authorized = True
            token = request.headers.get("Authorization")[4:]
            #return Response({"error": "Domaine invalide. Veuillez vérifier vos headers"}, status=status.HTTP_400_BAD_REQUEST)

        else: # Paramètre existant = tentative de connexion à une URL précise.
            host = request.headers.get("X-Requested-Host") # Lecture du domaine d'origine depuis les headers
            token = request.headers.get("Authorization")[4:]
            is_authorized, status_code = user_has_domain_access(request.user, host)

        if is_authorized :
            response = Response({"message": "Autorisation réussie avec succès."},status=status.HTTP_200_OK)
            response.set_cookie(
                "session_auth",
                value=token, # Characters excluding the "JWT " at the beginning of the Authorization header
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                domain= '.espificio.com',
                max_age=3600
            )
            return response

        elif (not is_authorized and status_code == 403) :
            return Response(
                {"error":f"L'autorisation a échoué : vous n'avez pas accès à {host}"},
                status=status.HTTP_403_FORBIDDEN
            )

        elif (not is_authorized and status_code == 404) :
            return Response(
                {"error": f"Le domaine {host} est introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        else :
            return Response(
                {"error" : "Requête invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class CheckCookieView(GenericAPIView):
    authentication_classes = [] # Allows connection without a JWT, from other websites
    permission_classes = [AllowAny]

    def get(self, request):
        if not "X-Request-URI" in request.headers:
            return Response({"error":"Domaine invalide. Veuillez vérifier vos headers."}, status=status.HTTP_400_BAD_REQUEST)
        if not "session_auth" in request.COOKIES:
            return Response({"error":"Le cookie session_auth est introuvable. Veuillez vérifier vos cookies"}, status=status.HTTP_401_UNAUTHORIZED)

        token = request.COOKIES.get("session_auth")
        host = request.headers.get("X-Request-URI")

        try :
            decoded = AccessToken(token) # This will raise an exception if the token is invalid.
            decoded = decoded.payload
            user_id = decoded.get("user_id") 
            user = User.objects.filter(id=user_id).first()

            is_authorized, status_code = user_has_domain_access(user, host)

        except TokenError:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        if is_authorized :
            return Response({"message": "Success!"}, status=status.HTTP_200_OK)

        elif (not is_authorized and status_code == 403) :
            return Response({"error":f"L'autorisation a échoué : vous n'avez pas accès à {host}"}, status=status.HTTP_403_FORBIDDEN)

        elif (not is_authorized and status_code == 404) :
            return Response({"error": f"Le domaine {host} est introuvable."}, status=status.HTTP_404_NOT_FOUND)

        else :
            return Response(
                {"error" : "Requête invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )
