# user/signals.py
import logging, requests
from django.core.cache import cache
from django.db import transaction
from django.urls import reverse
from django.dispatch import receiver
from djoser.signals import user_activated
from djoser.serializers import SendEmailResetSerializer

logger = logging.getLogger(__name__)

#@receiver(user_activated, dispatch_uid="user.user_activated", weak=False)
#def on_user_activated(sender, user, request, **kwargs):
#    """
#    Dès qu’un user est activé, on déclenche l’envoi de l’email de réinitialisation
#    via Djoser (qui utilisera user.emails.PasswordResetEmail selon tes settings).
#    """
#
#    def _send_reset_email():
#        # Idempotence (éviter les doublons si le signal est déclenché plusieurs fois)
#        key = f"password:reset-sent:{user.pk}"
#        # ex: 300s = 5 minutes (ajuste selon ton besoin)
#        if not cache.add(key, "1", timeout=300):
#            logger.info("[password] reset already sent recently for %s — skipping", user.email)
#            return
#
#        try:
#            # Djoser génère uid/token + url en fonction des settings :
#            # PROTOCOL=https, DOMAIN=arevagence.com,
#            # PASSWORD_RESET_CONFIRM_URL="auth/reset-password/{uid}/{token}"
#            ser = SendEmailResetSerializer(
#                data={user.__class__.EMAIL_FIELD: user.email},  # “email” par défaut
#                context={"request": request},  # => URLs absolues correctes
#            )
#            ser.is_valid(raise_exception=True)
#            ser.save()  # => appelle ta classe user.emails.PasswordResetEmail
#            logger.info("[password] reset email requested for %s via Djoser serializer", user.email)
#
#        except Exception:
#            logger.exception("[password] failed to request reset email for %s", user.email)
#
#    # On envoie seulement après commit réussi (évite liens créés pour un user non activé)
#    transaction.on_commit(_send_reset_email)
