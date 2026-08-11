from .models import ProfilUtilisateur, Domaine
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
import users

class ProfileSerializer(ModelSerializer):
    utilisateur_nom = ReadOnlyField(source="User.email")

    class Meta:
        model = ProfilUtilisateur
        fields = ['utilisateur_nom', 'nom']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['domaines'] = [domaines.nom for domaines in instance.domaines.all()]
        
        return representation
    
class DomainSerializer(ModelSerializer):
    class Meta:
        model = Domaine
        fields = '__all__'
