from djoser.email import (
    ActivationEmail as BaseActivationEmail,
    PasswordResetEmail as BasePasswordResetEmail,
)
from django.utils.encoding import force_str
from djoser.utils import encode_uid
from django.contrib.auth.tokens import default_token_generator
from user.tasks import send_djoser_email
from django.conf import settings
from urllib.parse import urljoin


def _build_base_url(protocol: str | None, domain: str | None) -> str:
    safe_protocol = protocol or settings.DJOSER.get("PROTOCOL") or "https"
    safe_domain = domain or settings.DJOSER.get("DOMAIN") or "localhost"
    return f"{safe_protocol}://{safe_domain}/"


def _build_media_url(base_url: str, relative_path: str) -> str:
    media_prefix = settings.MEDIA_URL.lstrip("/")
    return urljoin(base_url, f"{media_prefix}{relative_path}")


class ActivationEmail(BaseActivationEmail):
    #def get_connection(self, fail_silently=False, **kwargs):
    #    # force fail_silently=False quoiqu'il arrive
    #    return super().get_connection(fail_silently=False, **kwargs)

    def send(self, to):
        """
        Ne passe à Celery que des primitives JSON (pas d'objet user, pas de request).
        """
        ctx = dict(self.get_context_data() or {})
        user = ctx.get("user")

        uid = ctx.get("uid") or encode_uid(user.pk)
        token = ctx.get("token") or default_token_generator.make_token(user)

        base_be = _build_base_url("https", ctx.get("domain").lstrip("https://"))
        print(f"prefix : {base_be}")

        payload = {
            "kind": "activation",
            "to": to if isinstance(to, (list, tuple)) else [to],
            "user_id": user.pk,
            "uid": force_str(uid),
            "token": force_str(token),
            "activation_url": ctx.get("activation_url"),
            "site_name": "Authenticate",
            "domain": ctx.get("domain"),
            "protocol": ctx.get("protocol"),
        }
        send_djoser_email.delay(payload)
        print(f"email d'activation envoyé")


class PasswordResetEmail(BasePasswordResetEmail):
    """
    Email de réinitialisation de mot de passe personnalisé :
    - Envoie un payload complet à la tâche Celery.
    """

    def send(self, to):
        # Récupère le contexte enrichi (fusionné)
        ctx = self.get_context_data()
        user = ctx.get("user")
        base_be = _build_base_url(ctx.get("protocol"), ctx.get("domain"))
        print(f"prefix : {base_be}")

        # Prépare le payload envoyé à ton worker Celery
        payload = {
            "kind": "password_reset",
            "to": to if isinstance(to, (list, tuple)) else [to],
            "user_id": user.pk,
            "uid": force_str(ctx.get("uid") or ""),
            "token": force_str(ctx.get("token") or ""),
            "frontend_url": ctx.get("frontend_url"),
            "site_name": "Authenticate",
            "protocol": settings.DJOSER.get("PROTOCOL"),
            "domain": settings.DJOSER.get("DOMAIN"),
            "reset_url": ctx.get("reset_url") or ctx.get("url"),
        }
        print(f"kind: password_reset")
        print(f"to: {to if isinstance(to, (list, tuple)) else [to]}")
        print(f"user_id: {user.pk}")
        print(f"uid: {force_str(ctx.get("uid") or "")}")
        print(f"token: {force_str(ctx.get("token") or "")}")
        print(f"frontend_url: {ctx.get("frontend_url")}")
        print(f"protocol: {settings.DJOSER.get("PROTOCOL")}")
        print(f"domain: {settings.DJOSER.get("DOMAIN")}")
        print(f"reset_url: {ctx.get("reset_url") or ctx.get("url")}")       

        send_djoser_email.delay(payload)
        print(f"email de reset d'email envoyé")
        fe_url = ctx.get("reset_url") or ctx.get("url")
        print(type(fe_url))
        print(fe_url[5:])
