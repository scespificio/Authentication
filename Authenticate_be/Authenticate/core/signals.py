from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from core.models import UtilisateurExtension

'''@receiver(post_save, sender=User)
def ensure_utilisateur_extension(sender, instance, created, **kwargs):
    if created:
        UtilisateurExtension.objects.get_or_create(user=instance)'''