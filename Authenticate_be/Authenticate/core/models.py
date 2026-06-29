from django.db import models
import users

# Create your models here.

class Domaine(models.Model):
    nom = models.CharField(max_length=100)
    url = models.CharField(unique=True, max_length=100)

    def __str__(self) -> str:
        return self.nom

    class Meta:
        verbose_name = "Domaine"
        verbose_name_plural = "Domaines"


class ProfilUtilisateur(models.Model):
    utilisateur = models.ForeignKey(users.models.User, on_delete=models.CASCADE) # A modifier  : Plusieurs utilisateurs peuvent avoir le même profil_u VOIR AVEC STEVE SI L'INVERSE EST PAS PLUS LOGIQUE.
    nom = models.CharField(max_length=100)
    domaines = models.ManyToManyField(
        "Domaine",
        blank=True,
        related_name="profils",
        verbose_name="Domaines autorisés",
    )

    def __str__(self) -> str:
        return self.nom

    class Meta:
        verbose_name = "Profil Utilisateur"
        verbose_name_plural = "Profils Utilisateur"
