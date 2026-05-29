from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        print("[apps.ready] core signals loaded", flush=True)  # trace visible au boot
        from . import signals  # enregistre le receiver

