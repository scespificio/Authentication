from django.db import models
import users.models

# Create your models here.

class Société(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nom

    class Meta:
        verbose_name = "Modèle de société"
        verbose_name_plural = "Modèles de sociétés"

class Profil(models.Model):
    utilisateur = models.OneToOneField(users.models.User, on_delete=models.CASCADE)
    société = models.ForeignKey(Société, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nom

    class Meta:
        verbose_name = "Modèle de profil"
        verbose_name_plural = "Modèles de profils"

class Domaine(models.Model):
    société = models.ForeignKey(Société, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    url = models.CharField(unique=True, max_length=100)

    def __str__(self) -> str:
        return self.nom

    class Meta:
        verbose_name = "Modèle de domaine"
        verbose_name_plural = "Modèles de domaines"
