from django.apps import AppConfig


class userConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        print("[apps.ready] user signals loaded", flush=True)  # trace visible au boot
        from . import signals  # enregistre le receiver

