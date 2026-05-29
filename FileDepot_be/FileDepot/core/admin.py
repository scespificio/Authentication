from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from djoser.utils import encode_uid
from django.contrib.auth.tokens import default_token_generator
from .models import User , WebConfig , EmailTemplate, ChakraTemplate
from images.models import ImageItem
from images.admin import render_thumb
from tags.admin import TagsInline
import traceback
from django.template.loader import get_template
from django.conf import settings
from urllib.parse import urljoin
from core.services.activation import send_activation_email

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
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "is_superuser","config"]
    list_filter = ("is_active", "is_staff", "is_superuser","config")
    fieldsets = [
        (None, {
            "fields": ["first_name", "last_name", "email", "password"]
        }),
        (_("Profil de l'application"), {
            "fields": ["config"]
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



admin.site.register(ChakraTemplate, admin.ModelAdmin)

@admin.register(EmailTemplate)  # équivaut à admin.site.register(WebConfig, WebConfigAdmin)
class EmailTemplateAdmin(admin.ModelAdmin):
    # Minimal, ne référence aucun champ incertain
    list_display = ("__str__","description")   # affiche la représentation texte


@admin.action(description="Dupliquer")
def duplicate_webconfig(modeladmin, request, queryset):
    for obj in queryset:
        original_name = obj.name  # garde le nom original
        try:
            obj.pk = None  # pour dupliquer
            obj.name = f"{original_name}_copy"
            obj.save()
            modeladmin.message_user(request, f"WebConfig '{obj}' dupliquée avec succès.", messages.SUCCESS)
        except Exception as e:
            modeladmin.message_user(request, f"Erreur lors de la duplication de '{obj}': {e}", messages.ERROR)
            traceback.print_exc()


@admin.register(WebConfig)  # équivaut à admin.site.register(WebConfig, WebConfigAdmin)
class WebConfigAdmin(admin.ModelAdmin):
    # Minimal, ne référence aucun champ incertain
    list_display = ("__str__","tag_name")   # affiche la représentation texte
    ordering = ("id",)            # tri par clé primaire
    inlines = [TagInline, LogoInline]
    actions = [duplicate_webconfig]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Précharge les TaggedItem + Tag pour éviter 1 requête par ligne
        return qs.prefetch_related("tags_rel__tag")

    @admin.display(description="Tag")
    def tag_name(self, obj):
        ti = obj.tags_rel.all().first()  # déjà préchargé via get_queryset
        return getattr(getattr(ti, "tag", None), "label", "—")



class ProductImageInline(ImageInline):
    # Ouvre une popup de recherche/sélection pour l'image
    raw_id_fields = ['image']

    fields = ['image', 'thumb',"image_tags", 'created_at', 'display_order']
    readonly_fields = ImageInline.readonly_fields + ["image_tags"]
    extra = 1      # 1 formulaire vide
    max_num = 5   # empêche Django de proposer plusieurs vides

class CategoryImageInline(ImageInline):
    fields = ['image', "image_tags", 'thumb', 'created_at']
    readonly_fields = ImageInline.readonly_fields + ["image_tags"]
    extra = 1      # 1 formulaire vide
    max_num = 3    # empêche Django de proposer plusieurs vides
