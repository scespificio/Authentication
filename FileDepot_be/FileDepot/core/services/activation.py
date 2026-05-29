from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin    
from django.utils.translation import gettext_lazy as _
from djoser.utils import encode_uid
from django.contrib.auth.tokens import default_token_generator
import traceback
from django.conf import settings
from urllib.parse import urljoin
from djoser.conf import settings as djoser_settings
from djoser.compat import get_user_email

def abs_media(request, path):
    base = settings.MEDIA_URL.rstrip("/")
    return request.build_absolute_uri(f"{base}/{path.lstrip('/')}")

def send_activation_email(request, queryset):
    envoyes, ignores = 0, 0

    for user in queryset:
        email = get_user_email(user)
        
        if user.is_active or not email or not user.has_usable_password():
            ignores += 1
            continue

        try:
            # 1) Contexte “de base” de Djoser (peut fournir uid/token selon versions)
            base_email = djoser_settings.EMAIL.activation(request, {"user": user})
            try:
                base_ctx = base_email.get_context_data()
            except Exception:
                base_ctx = {}


            # 2) uid + token (on s'assure de les avoir)
            uid = base_ctx.get("uid") or encode_uid(user.pk)
            token = base_ctx.get("token") or default_token_generator.make_token(user)

            # 3) Construit l'URL FRONTEND d'activation: /activation/:uid/:token
            frontend_base = settings.FRONTEND_BASE_URL.rstrip("/") + "/"
            rel_path = f"activate/{uid}/{token}"
            activation_url = urljoin(frontend_base, rel_path)  # ex: https://app.exemple.com/activation/uid/token

            print("Activation URL:", activation_url)
            # 4) Contexte FINAL pour le template d’e-mail
            ctx = {
                **base_ctx,
                "user": user,
                # Certains templates attendent `url`, d'autres `activation_url`
                "url": activation_url,
                "activation_url": activation_url,
                # Optionnel: même valeur pour affichage d’un “label”
                "label_url": activation_url,
                # Logo absolu si ton template l'utilise
                "logo_url": abs_media(request, "images/logo.png"), # Placeholder pour le logo
                # Souvent utile
                "site_name": getattr(settings, "SITE_NAME", "Mon site"),
                "domain": frontend_base.rstrip("/"),
                # On expose aussi uid/token au cas où le template les demande
                "uid": uid,
                "token": token,
                "failed_silently": False
            }

 
            # 5) Recrée l’objet email avec le contexte final puis envoie
            email_obj = djoser_settings.EMAIL.activation(request, ctx)
            email_obj.send(to=[email])
            envoyes += 1
        except Exception as exc:
            traceback.print_exc()
            messages.error(request, f"Échec pour {user}: {exc}")

    if envoyes:
        messages.success(request, f"{envoyes} e-mail(s) d’activation envoyé(s).")
    if ignores:
        messages.warning(
            request,
            f"{ignores} utilisateur(s) ignoré(s) (actifs, sans e-mail ou MP inutilisable)."
        )

def send_password_email(request, user):
    email = get_user_email(user)
    try:
        base_email = djoser_settings.EMAIL.password_reset(request, {"user": user})
        try:
            base_ctx = base_email.get_context_data()
        except Exception:
            base_ctx = {}

        # 2) uid + token (on s'assure de les avoir)
        uid = base_ctx.get("uid") or encode_uid(user.pk)
        token = base_ctx.get("token") or default_token_generator.make_token(user)
        # 3) Construit l'URL FRONTEND d'activation: /activation/:uid/:token
        frontend_base = settings.FRONTEND_BASE_URL.rstrip("/") + "/"
        rel_path = f"resetpassword/{uid}/{token}"
        reset_url = urljoin(frontend_base, rel_path)  # ex: https://app.exemple.com/activation/uid/toke
        # 4) Contexte FINAL pour le template d’e-mail
        ctx = {
            **base_ctx,
            "user": user,
            # Certains templates attendent `url`, d'autres `activation_url`
            "url": reset_url,
            # Optionnel: même valeur pour affichage d’un “label”
            "logo_url": abs_media(request, "images/Logo.png"), # Placeholder pour le logo
            # Souvent utile
            "site_name": getattr(settings, "SITE_NAME", "Mon site"),
            "domain": frontend_base.rstrip("/"),
            # On expose aussi uid/token au cas où le template les demande
            "uid": uid,
            "token": token,
        }
        print("Password reset URL:", reset_url)
        # 5) Recrée l’objet email avec le contexte final puis envoie
        email_obj = djoser_settings.EMAIL.password_reset(request, ctx)
        email_obj.send([email],fail_silently=False)

    except Exception as exc:
        traceback.print_exc()
        messages.error(request, f"Échec pour {user}: {exc}")
