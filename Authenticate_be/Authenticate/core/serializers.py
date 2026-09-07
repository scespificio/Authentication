from rest_framework.serializers import ModelSerializer, ReadOnlyField

from .models import Domain, UserIAM


class ProfileSerializer(ModelSerializer):
    utilisateur_nom = ReadOnlyField(source="User.email")

    class Meta:
        model = UserIAM
        fields = ["utilisateur_nom", "nom"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["domaines"] = [
            domaines.nom for domaines in instance.domaines.all()
        ]

        return representation


class DomainSerializer(ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"
