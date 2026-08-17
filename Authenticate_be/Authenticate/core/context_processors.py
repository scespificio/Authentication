from django.conf import settings


def frontend_base_url(request):
    """
    Rend disponible FRONT_END_URL dans tous les templates.
    """
    return {"FRONTEND_BASE_URL": getattr(settings, "FRONTEND_BASE_URL", "")}
