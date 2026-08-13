from django.conf import settings
from django.db import models


class Domaine(models.Model):
    nom = models.CharField(max_length=100)
    url = models.CharField(
        unique=True,
        max_length=100,
        help_text="Renseigner sous la forme DOMAINE/SOUS-DOMAINE sans '/' à la fin.",
    )

    def __str__(self) -> str:
        return self.nom

    class Meta:
        verbose_name = "Domaine"
        verbose_name_plural = "Domaines"


class DroitUtilisateur(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authenticate_profile",
    )
    # nom = models.CharField(max_length=100)
    domaines = models.ManyToManyField(
        "Domaine",
        blank=True,
        related_name="droits",
        verbose_name="Domaines autorisés",
    )

    def __str__(self) -> str:
        return str(self.user)

    class Meta:
        verbose_name = "Droit Utilisateur"
        verbose_name_plural = "Droits Utilisateur"


"""class UtilisateurExtension(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="utilisateur_extension",
    )>
    profil = models.ForeignKey(
        ProfilUtilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return str(self.user)"""
