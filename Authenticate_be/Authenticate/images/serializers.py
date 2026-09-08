from rest_framework.relations import PrimaryKeyRelatedField  # noqa: EXE002
from rest_framework.serializers import ModelSerializer

from .models import Image, ImageItem


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "title", "image_file", "uploaded_at")


class ImageItemSerializer(ModelSerializer):
    """
    Serializer utilisé à l'intérieur de ProductSerializer.
    On expose l'image (lecture) + image_id (écriture).
    """

    image = ImageSerializer(read_only=True)
    image_id = PrimaryKeyRelatedField(
        queryset=Image.objects.all(), source="image", write_only=True
    )

    class Meta:
        model = ImageItem
        # content_type, object_id et content_object sont gérés automatiquement
        read_only_fields = ("id", "created_at")
        fields = (
            "id",
            "description",
            "display_order",
            "created_at",
            "image",  # lecture
            "image_id",  # écriture
        )
