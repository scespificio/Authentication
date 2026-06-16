from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from djoser.utils import encode_uid
from django.contrib.auth.tokens import default_token_generator
from .models import User , EmailTemplate
from images.models import ImageItem
from images.admin import render_thumb
from tags.admin import TagsInline
import traceback
from django.template.loader import get_template
from django.conf import settings
from urllib.parse import urljoin
from user.services.activation import send_activation_email

from djoser.conf import settings as djoser_settings
from djoser.compat import get_user_email

User = get_user_model()

@admin.action(description="Envoyer un e-mail d’activation du compte")
def send_activation_email_from_admin(modeladmin, request, queryset):
    send_activation_email(request, queryset)

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "is_superuser"]
    list_filter = ("is_active", "is_staff", "is_superuser")
    fieldsets = [
        (None, {
            "fields": ["first_name", "last_name", "email", "password"]
        }),
        (_("Status"), {
            "fields": ["is_active", "is_staff", "is_superuser", "groups"]
        }),
    ]
    actions = [send_activation_email_from_admin]
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name"),
        }),
    )

    search_fields = ["first_name", "last_name", "email"]
    ordering = ["first_name", "last_name"]

class TagInline(TagsInline):
    max_num = 1  # evite de saisir plusieurs tags de profils

class ImageInline(GenericTabularInline):
    model = ImageItem
    readonly_fields = ['created_at', 'thumb']

    @admin.display(description="Aperçu")
    def thumb(self, obj):
        if obj and obj.image_id and obj.image and obj.image.image_file:
            return render_thumb(obj.image.image_file)
        return "—"

    @admin.display(description="Tags de l’image")
    def image_tags(self, obj: ImageItem):
        if not obj or not obj.image_id:
            return "—"
        labels = obj.image.taggings.values_list("tag__label", flat=True)
        return ", ".join(sorted(set(labels))) if labels else "—"

class LogoInline(ImageInline):
    raw_id_fields = ['image']
    fields = ['image', "image_tags", 'thumb', 'created_at']
    readonly_fields = ImageInline.readonly_fields + ["image_tags"]
    extra =  0     # 1 formulaire vide
    max_num = 1    # empêche Django de proposer plusieurs vide

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    # Minimal, ne référence aucun champ incertain
    list_display = ("__str__","description")   # affiche la représentation texte