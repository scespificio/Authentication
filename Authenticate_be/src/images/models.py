from django.contrib.contenttypes.fields import (  # noqa: EXE002
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from tags.models import TaggedItem


# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=100)
    image_file = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    taggings = GenericRelation(TaggedItem, related_query_name="images")

    def __str__(self):
        return self.title


class ImageItem(models.Model):
    image = models.ForeignKey(
        Image, related_name="imageitems", on_delete=models.CASCADE
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    display_order = models.PositiveSmallIntegerField(_("ordre d'affichage"), default=0)

    # Generic relation fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Item for {self.image.title}"
