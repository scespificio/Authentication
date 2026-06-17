from django.shortcuts import render
from rest_framework.generics  import GenericAPIView
from .models import Société, Profil, Domaine
from .serializers import CompanySerializer, ProfileSerializer, DomainSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CompanyView(GenericAPIView): # GET list
    serializer_class = CompanySerializer
    queryset = Société.objects.all()

    def get(self, request):
        obj = self.get_queryset().filter(utilisateur=request.user)
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)

class ProfileView(GenericAPIView): # GET list
    serializer_class = ProfileSerializer
    queryset = Profil.objects.all()

    def get(self, request):
        obj = self.get_queryset().filter(utilisateur=request.user)
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)


class DomainView(GenericAPIView): # GET list
    serializer_class = DomainSerializer
    queryset = Domaine.objects.all()

    def get(self, request):
        obj = self.get_queryset().filter(utilisateur=request.user)
        return Response({"results": self.get_serializer(obj, many=True).data}, status=status.HTTP_200_OK)
