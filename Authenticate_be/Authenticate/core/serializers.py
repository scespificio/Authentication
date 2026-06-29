from .models import ProfilUtilisateur, Domaine
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
import users

class CoreTokenObtainPairSerializer(ModelSerializer): # Faire hériter du sérialiseur dans users.serializers.py pour récupérer l'utilisateur et l'URL slug. Si l'utilisateur n'a pas l'url slug dans ses url autorisées, retourne 404, sinon 201. On doit le faire ici car c'est apr-s super().validate() qu'on sait qui est connecté, et que le mdp est correct.
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs): 
        data = super().validate(attrs)  # {'refresh': '...', 'access': '...'}
        # Sérialise l'user + insère les tokens via le context
        user_data = users.serializers.UserSerializer( # A FAIRE ICI Récupérer l'utilisateur et l'URL slug. Si l'utilisateur n'a pas l'url slug dans ses url autorisées, retourne 404, sinon 201. On doit le faire ici car c'est apr-s super().validate() qu'on sait qui est connecté, et que le mdp est correct.
            self.user,
            context={'request': self.context.get('request'), 'tokens': data}
        ).data

        return {
            **user_data,
            'access_token': str(data.get('access')),
            'refresh_token': str(data.get('refresh')),
        }

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
