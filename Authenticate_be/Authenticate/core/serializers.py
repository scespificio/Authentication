from .models import Profil, Société, Domaine
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField

class ProfileSerializer(ModelSerializer):
    utilisateur_nom = ReadOnlyField(source="User.email")
    société_nom = ReadOnlyField(source="Société.nom")

    class Meta:
        model = Profil
        fields = ['id', 'utilisateur_nom', 'société_nom', 'nom']

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Société
        fields = ['id', 'nom']

class DomainSerializer(ModelSerializer):
    société_nom = ReadOnlyField(source="Société.nom")

    class Meta:
        model = Domaine
        fields = ['id', 'société_nom', 'nom', 'domaine']