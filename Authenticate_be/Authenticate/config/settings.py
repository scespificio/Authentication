from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

def env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG') == 'True'

# Internationalization
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = "fr"
LANGUAGES = [
    ("fr", "Français"),
    ("en", "English"),
]

DJANGO_ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS")
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS")

if DJANGO_ALLOWED_HOSTS:
    ALLOWED_HOSTS = [h.strip() for h in DJANGO_ALLOWED_HOSTS.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = []

if CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS = [h.strip() for h in CORS_ALLOWED_ORIGINS.split(",") if h.strip()]
else:
    CORS_ALLOWED_ORIGINS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    "rest_framework_simplejwt.token_blacklist",
    'django.contrib.staticfiles',
    'corsheaders',
    'images.apps.ImagesConfig',
    'tags.apps.TagsConfig',
    'users.apps.UsersConfig',
    'debug_toolbar',
    'djoser'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
                'users.context_processors.frontend_base_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
    }
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        #"rest_framework.authentication.SessionAuthentication",
        #"rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

if DEBUG:
    # En dev : API navigable + JSON
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ]
else:
    # En prod : API seulement JSON → pas de browsable API
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer",
    ]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "users.User"
# Static files (CSS, JS, images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # dossier où collectstatic va tout mettre

# Si tu as des fichiers statiques "source" dans un dossier /static de ton projet :
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Médias (uploads)
MEDIA_URL = "/uploads/"
if DEBUG:
    MEDIA_ROOT = (BASE_DIR.parent / "uploads").resolve()
else:
    MEDIA_ROOT = (BASE_DIR / "uploads").resolve()
MEDIA_ROOT = BASE_DIR / "uploads"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJOSER = {
    'SEND_ACTIVATION_EMAIL' : True,
    'ACTIVATION_URL': 'auth/activate/{uid}/{token}', 
    "PASSWORD_RESET_CONFIRM_URL": "auth/reset-password/{uid}/{token}",
    "DOMAIN": os.getenv("FRONTEND_DOMAIN"),
    "SITE_NAME": "Authenticate",
    "EMAIL": {"activation": "users.emails.ActivationEmail",
              "password_reset": "users.emails.PasswordResetEmail"},
    "PROTOCOL": os.getenv("FRONTEND_PROTOCOL"),
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
        'current_user': 'users.serializers.UserSerializer',
    }
}

PASSWORD_RESET_TIMEOUT = int(os.getenv("PASSWORD_RESET_TIMEOUT", 86400))  # 24 hours default

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME':timedelta(seconds=int(os.getenv("ACCESS_TOKEN_LIFETIME", 900))), 
    'REFRESH_TOKEN_LIFETIME':timedelta(seconds=int(os.getenv("REFRESH_TOKEN_LIFETIME", 1800))),
    'BLACKLIST_AFTER_ROTATION': False
}

# Celery en mode synchrone, sans broker (DEV UNIQUEMENT)
#CELERY_TASK_ALWAYS_EAGER = True
#CELERY_TASK_EAGER_PROPAGATES = True  # remonte les exceptions dans Django
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://authenticate-redis-broker:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://authenticate-redis-broker:6379/1")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
POSTMARK_SMTP_TOKEN = (os.getenv("POSTMARK_SMTP_TOKEN") or os.getenv("POSTMARK_SERVER_API_TOKEN") or "").strip()
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.postmarkapp.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = (os.getenv("EMAIL_HOST_USER") or POSTMARK_SMTP_TOKEN or "").strip() or None
EMAIL_HOST_PASSWORD = (os.getenv("EMAIL_HOST_PASSWORD") or POSTMARK_SMTP_TOKEN or "").strip() or None
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)
if EMAIL_USE_TLS and EMAIL_USE_SSL:
    raise ValueError("EMAIL_USE_TLS et EMAIL_USE_SSL ne peuvent pas être activés en même temps.")
DEFAULT_FROM_EMAIL = os.getenv("POSTMARK_FROM_EMAIL")
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "40"))
SERVER_EMAIL = DEFAULT_FROM_EMAIL

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# Sécurité HTTPS
SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "False") == "True"

# Django derrière un reverse proxy HTTPS (Nginx)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "http")
USE_X_FORWARDED_HOST = True

if SECURE_SSL_REDIRECT:
    # Cookies protégés (uniquement sous HTTPS)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# CSRF trusted origins (facultatif mais recommandé)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]