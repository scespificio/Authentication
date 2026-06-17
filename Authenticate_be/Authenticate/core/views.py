from django.shortcuts import render
from django.conf import settings
from .models import Société, Profil, Domaine
from .serializers import CompanySerializer, ProfileSerializer, DomainSerializer

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics  import GenericAPIView
from rest_framework.decorators import action

from dotenv import load_dotenv
import os
import json

load_dotenv()

CONFIG_FOLDER = os.getenv('CONFIG_FILE_FOLDER')
CONFIG_FILE = os.getenv('CONFIG_FILE_NAME')

# Create your views here.

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

class CompanyView(GenericAPIView): # GET all
    serializer_class = CompanySerializer
    queryset = Société.objects.all()

    def get(self, request):
        obj = self.get_queryset()
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)

class CompanyViewDetail(GenericAPIView): # GET one
    serializer_class = CompanySerializer
    queryset = Société.objects.all()

    def get(self, request):
        obj = self.get_queryset().filter(profil__utilisateur=request.user).distinct() # The user can only see the company they belong to
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)

class ProfileView(GenericAPIView): # GET all
    serializer_class = ProfileSerializer
    queryset = Profil.objects.all()

    def get(self, request):
        obj = self.get_queryset()
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)

class ProfileViewDetail(GenericAPIView): # GET one
    serializer_class = ProfileSerializer
    queryset = Profil.objects.all()

    def get(self, request):
        obj = self.get_queryset().filter(utilisateur=request.user)
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)

class DomainView(GenericAPIView): # GET list
    serializer_class = DomainSerializer
    queryset = Domaine.objects.all()

    def get(self, request):
        obj = self.get_queryset().filter(société__profil__utilisateur=request.user).distinct()
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)
