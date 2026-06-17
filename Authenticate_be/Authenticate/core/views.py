from django.shortcuts import render
from rest_framework.generics  import GenericAPIView
from .models import Société, Profil, Domaine
from .serializers import CompanySerializer, ProfileSerializer, DomainSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

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
