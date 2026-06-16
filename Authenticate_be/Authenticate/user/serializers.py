from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer, SendEmailResetSerializer
from rest_framework.serializers import ModelSerializer,SerializerMethodField, Serializer, CharField
from django.contrib.contenttypes.models import ContentType
from images.serializers import ImageItemSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.utils import decode_uid
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [ 'email', 'password',
                   'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['email', 'first_name', 'last_name']

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Si ton USERNAME_FIELD = 'email', ça marchera tel quel.
    # Sinon, dé-commente ce __init__ pour accepter "email" au lieu de "username".
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'] = serializers.EmailField()
    #     self.fields.pop('username', None)

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):
        # Si tu as gardé le __init__ ci-dessus :
        # attrs['username'] = attrs.pop('email', attrs.get('username'))
        data = super().validate(attrs)  # {'refresh': '...', 'access': '...'}
        # Sérialise l'user + insère les tokens via le context
        user_data = UserSerializer(
            self.user,
            context={'request': self.context.get('request'), 'tokens': data}
        ).data

        return {
            **user_data,
            'access_token': str(data.get('access')),
            'refresh_token': str(data.get('refresh')),
        }