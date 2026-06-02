from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from tags.models import TaggedItem
from pathlib import Path
from images.models import ImageItem
import uuid
from datetime import date as dt

def get_default_config():
    return {}

class UserManager(BaseUserManager):
    """Manager personnalisé pour User avec email comme identifiant"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("L'adresse email doit être renseignée"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Le superuser doit avoir is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Le superuser doit avoir is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

# Create your models here.
class User(AbstractUser):
    username = None  # on n'utilise pas le champ username de Django
    email = models.EmailField(_("Adresse e-mail"), unique=True)
    is_staff = models.BooleanField(
        _("Membre"),
        default=False,
        help_text=_("Indique si l'utilisateur peut se connecter au site d’administration de la plateforme."),
    )
    is_superuser = models.BooleanField(
        _("Administrateur Plateforme"),
        default=False,
        help_text=_("Indique que cet utilisateur a tous les droits"),
    )

    config = models.ForeignKey("WebConfig", 
                               verbose_name=_("parametrage"),
                               help_text=_("Preciser le profil d'application à utiliser pour cet utilisateur"),
                               blank=True, null=True, on_delete=models.SET_NULL, related_name="users")

    USERNAME_FIELD = "email"        # champ utilisé pour l'authentification
    REQUIRED_FIELDS = []            # pas d'autre champ obligatoire

    objects = UserManager()         # on attache le manager custom

    def __str__(self):
        return self.email
  
    class Meta:
      verbose_name = _("Utilisateur")
      verbose_name_plural = _("Utilisateur")

class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    footer = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Modèle d’email"
        verbose_name_plural = "Modèles d’email"

class ChakraTemplate(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    chakra = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Modèle d’UI"
        verbose_name_plural = "Modèles d’UI"

    def __str__(self) -> str:
        return self.name

class WebConfig(models.Model):
    name = models.CharField(_("nom"), max_length=100)
    logo = GenericRelation(ImageItem, related_query_name="for_Webconfig")
   
    ui_template = models.ForeignKey(ChakraTemplate,
                               verbose_name=_("Modèle d’UI"),
                               help_text=_("Modèle d’interface utilisateur à utiliser pour cette application"),
                               blank=True, null=True, on_delete=models.SET_NULL, related_name="ui_templates")


    config = models.JSONField(_("configuration"), default=get_default_config)
    tags_rel = GenericRelation(TaggedItem, related_query_name="profils") 

    @property
    def logo_item(self):
        return self.logo.first() 

    @property
    def tagged_item(self):
        # ergonomie façon OneToOne : 0..1 objet
        return self.tags_rel.first()
    
    class Meta:
        ordering = ["name"]
        verbose_name = _("Profil")
        verbose_name_plural = _("Profils")

    def __str__(self):
        return f"{self.name}"

class Fichier(models.Model):
    utilisateur = models.ForeignKey(User, verbose_name="Utilisateur déposant", blank=True, null=True, on_delete=models.SET_NULL)
    nom = models.CharField(verbose_name="Nom", max_length=100, unique=True)
    date_creation = models.DateField(verbose_name="Date de création", default=dt.today, help_text="Format dd/mm/yyyy")
    horodatage_creation = models.TimeField(verbose_name="Heure de création", auto_now_add=True, help_text="Format HH:MM")
    chemin = models.TextField(verbose_name="Chemin système")
    chemin_destinataire = models.TextField(verbose_name="Chemin système chez le client", blank=True, null=True)
    
    class Meta:
        ordering = ["date_creation"]
        verbose_name = _("Fichier")
        verbose_name_plural = _("Fichiers")

    def __str__(self):
        return f"{self.nom}"