import os
from celery import Celery

# --- DIAG 1: trace le module de settings utilisé
# Aligne ce nom EXACTEMENT sur ton package et ton settings réels
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FileDepot.settings")
print("[celery.py] DJANGO_SETTINGS_MODULE =", os.environ.get("DJANGO_SETTINGS_MODULE"))

app = Celery("FileDepot")

# Charge la config depuis Django (clés préfixées CELERY_)
app.config_from_object("django.conf:settings", namespace="CELERY")

# --- DIAG 2: imprime ce que Django expose ET ce que Celery voit
try:
    from django.conf import settings
    print("[celery.py] Django flags (settings):",
          getattr(settings, "CELERY_TASK_ALWAYS_EAGER", None),
          getattr(settings, "CELERY_TASK_EAGER_PROPAGATES", None))
except Exception as e:
    print("[celery.py] Impossible d'importer django.conf.settings au chargement:", repr(e))

print("[celery.py] Celery sees (app.conf):",
      app.conf.task_always_eager, app.conf.task_eager_propagates)
print("[celery.py] Broker URL:", getattr(app.conf, "broker_url", None))
print("[celery.py] Result backend:", getattr(app.conf, "result_backend", None))

# (Option DEV uniquement) Forcer l'eager si le flag est présent côté settings
try:
    from django.conf import settings
    if getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False):
        app.conf.task_always_eager = True
        app.conf.task_eager_propagates = getattr(settings, "CELERY_TASK_EAGER_PROPAGATES", True)
        print("[celery.py] Forced eager ->",
              app.conf.task_always_eager, app.conf.task_eager_propagates)
except Exception:
    pass

# Découverte automatique des tasks.py
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print("Request:", repr(self.request))
