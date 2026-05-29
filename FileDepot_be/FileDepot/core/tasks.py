from celery import shared_task
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

@shared_task
def send_email(subject, html_message, to, cc=None, bcc=None, from_email=None, reply_to=None):
    sender = from_email or settings.DEFAULT_FROM_EMAIL
    plain_message = strip_tags(html_message)
    email = EmailMultiAlternatives(str(subject), plain_message, sender, to, cc=cc, bcc=bcc, reply_to=reply_to)
    email.attach_alternative(html_message, 'text/html')
    return email.send()


@shared_task
def send_djoser_email(payload: dict):
    """
    Reconstruit l'email Djoser côté worker et l'envoie.
    payload ne doit contenir que des primitives JSON.
    """
    kind = payload["kind"]
    to = payload["to"]

    # Recharge l'utilisateur côté worker (évite de sérialiser l'instance)
    User = get_user_model()
    user = User.objects.get(pk=payload["user_id"])
    reset_url = payload.get("reset_url")
    fe_url = reset_url[5:] if reset_url else None
    activation_url = payload.get("activation_url")

    # Contexte attendu par les templates Djoser
    context = {
        "user": user,
        "uid": payload.get("uid"),
        "token": payload.get("token"),
        "activation_url": activation_url,
        "reset_url": reset_url,
        "url": activation_url,
        "site_name": payload.get("site_name"),
        "domain": payload.get("domain"),
        "protocol": payload.get("protocol"),
        "logo_url": payload.get("logo_url"),
        "bg_url": payload.get("bg_url"),
        "fe_url": fe_url,    #retire le prefixe /auth qui provoquerait une redirection vers le back end par le proxy
    }


    # ⚠️ Utilise les classes Djoser d'ORIGINE (pas ta sous-classe) pour éviter la récursion.
    if kind == "activation":
        from djoser.email import ActivationEmail as DjoserActivationEmail
        email_obj = DjoserActivationEmail(request=None, context=context)
    elif kind == "password_reset":
        from djoser.email import PasswordResetEmail as DjoserPasswordResetEmail
        email_obj = DjoserPasswordResetEmail(request=None, context=context)
    else:
        raise ValueError(f"Unknown kind: {kind}")

    return email_obj.send(to)
