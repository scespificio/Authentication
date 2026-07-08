from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from .models import ProfilUtilisateur, Domaine
from .serializers import ProfileSerializer, DomainSerializer, CoreTokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics  import GenericAPIView
from rest_framework.decorators import action
from users.serializers import CustomTokenObtainPairSerializer
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView

from dotenv import load_dotenv
import os
import json

load_dotenv()

CONFIG_FOLDER = os.getenv('CONFIG_FILE_FOLDER')
CONFIG_FILE = os.getenv('CONFIG_FILE_NAME')

# Create your views here.
    
class CoreTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


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
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)

class ProfileViewDetail(GenericAPIView): # GET one
    serializer_class = ProfileSerializer
    queryset = ProfilUtilisateur.objects.all()

    def get(self, request):
        obj = self.get_queryset().filter(utilisateur=request.user)
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)

class DomainView(GenericAPIView): # GET all (TEMPORAIRE)
    serializer_class = DomainSerializer
    queryset = Domaine.objects.all()

    def get(self, request):
        obj = self.get_queryset()
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)

class AuthorizeView(GenericAPIView):# GET response
    def get(self, request):

        if not "X-Requested-Host" in request.headers:
            return Response({"error": "Domaine invalide. Veuillez vérifier vos headers"}, status=status.HTTP_400_BAD_REQUEST)

        host = request.headers.get("X-Requested-Host") # Lecture du domaine d'origine depuis les headers
        domain = Domaine.objects.filter(url=host).first()

        if not domain :
            return Response({"error": f"Le domaine {host} est introuvable."},status=status.HTTP_404_NOT_FOUND)

        is_authorized = ProfilUtilisateur.objects.filter(Q(utilisateur=request.user), Q(domaines=domain)).exists()

        if is_authorized :
            response = Response({"message": "Autorisation réussie avec succès.", "authorized":True},status=status.HTTP_200_OK)
            response.set_cookie(
                "session_auth",
                value=generated_token,
                httponly=True,
                secore=True,
                samesite="Lax",
                domain=host,
                max_age=3600
            )
            return response
        else :
            return Response(
                {"error":f"L'autorisation a échoué : vous n'avez pas accès à {host}"},
                status=status.HTTP_401_UNAUTHORIZED
            )