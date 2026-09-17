import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

# ---------------------------------------------------------
# Chargement des variables d'environnement
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Paramètres USERS
# ---------------------------------------------------------

from .users_settings import (
    ACTIVATION_MAIL_BODY,  # noqa: F401
    AUTH_USER_MODEL,  # noqa: F401
    USER_GROUP_DISPLAY,  # noqa: F401
    USERS_ENABLE_ACTIVATION_EMAIL,
    USERS_LOGIN_FIELD,  # noqa: F401
)

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)

    if raw is None:
        return default

    return raw.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


# ---------------------------------------------------------
# Base
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------
# Sécurité
# ---------------------------------------------------------

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = env_bool(
    "DJANGO_DEBUG",
    False,
)


# ---------------------------------------------------------
# Nom du service
# ---------------------------------------------------------
SERVICE_NAME = os.getenv("SERVICE_NAME", "Portail d’accès sécurisé")
DJANGO_APP_NAME = SERVICE_NAME

# ---------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------

TIME_ZONE = os.getenv(
    "DJANGO_TIME_ZONE",
    "UTC",
)

USE_TZ = True
USE_I18N = True
USE_L10N = True

LANGUAGE_CODE = "fr"

LANGUAGES = [
    ("fr", "Français"),
    ("en", "English"),
]


# ---------------------------------------------------------
# Hosts
# ---------------------------------------------------------

DJANGO_ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "",
)

ALLOWED_HOSTS = [
    host.strip() for host in DJANGO_ALLOWED_HOSTS.split(",") if host.strip()
]


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

cors_origins = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "",
)

CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in cors_origins.split(",") if origin.strip()
]

CORS_ALLOW_CREDENTIALS = env_bool(
    "CORS_ALLOW_CREDENTIALS",
    False,
)

CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-Requested-Host",
]


# ---------------------------------------------------------
# Applications
# ---------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django.contrib.staticfiles",
    "corsheaders",
    "users.apps.UsersConfig",
    "djoser",
    "core.apps.CoreConfig",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]


# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

# ---------------------------------------------------------
# Debug Toolbar
# ---------------------------------------------------------

INTERNAL_IPS = [
    "127.0.0.1",
]


# ---------------------------------------------------------
# URLs / WSGI
# ---------------------------------------------------------

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "core.context_processors.frontend_base_url",
            ],
        },
    },
]


# ---------------------------------------------------------
# Base de données
# ---------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# ---------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "15/min",
    },
}


if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ]
else:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer",
    ]


# ---------------------------------------------------------
# Validation des mots de passe
# ---------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]


# ---------------------------------------------------------
# Fichiers statiques
# ---------------------------------------------------------

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

# STATICFILES_DIRS = [
#    BASE_DIR / "static",
# ]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


## ---------------------------------------------------------
## Médias / uploads
## ---------------------------------------------------------
#
# MEDIA_URL = "/uploads/"
#
# if DEBUG:
#    MEDIA_ROOT = (BASE_DIR.parent / "uploads").resolve()
# else:
#    MEDIA_ROOT = (BASE_DIR / "uploads").resolve()


# ---------------------------------------------------------
# Django
# ---------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------
# Djoser
# ---------------------------------------------------------

DJOSER = {
    "SEND_ACTIVATION_EMAIL": USERS_ENABLE_ACTIVATION_EMAIL,
    "ACTIVATION_URL": "auth/activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": ("auth/reset-password/{uid}/{token}"),
    "DOMAIN": os.getenv("FRONTEND_DOMAIN"),
    "SITE_NAME": "Authenticate",
    "EMAIL": {
        "activation": "users.emails.ActivationEmail",
        "password_reset": "users.emails.PasswordResetEmail",
    },
    "PROTOCOL": os.getenv(
        "FRONTEND_PROTOCOL",
        "https",
    ),
    "SERIALIZERS": {
        "user_create": ("users.serializers.UserCreateSerializer"),
        "current_user": ("users.serializers.UserSerializer"),
    },
}


# ---------------------------------------------------------
# Password reset
# ---------------------------------------------------------

PASSWORD_RESET_TIMEOUT = int(
    os.getenv(
        "PASSWORD_RESET_TIMEOUT",
        "86400",
    )
)


# ---------------------------------------------------------
# JWT
# ---------------------------------------------------------

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(
        seconds=int(
            os.getenv(
                "ACCESS_TOKEN_LIFETIME",
                "900",
            )
        )
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        seconds=int(
            os.getenv(
                "REFRESH_TOKEN_LIFETIME",
                "1800",
            )
        )
    ),
    "BLACKLIST_AFTER_ROTATION": False,
}


# ---------------------------------------------------------
# Celery
# ---------------------------------------------------------

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL",
    "redis://authenticate-redis-broker:6379/0",
)

CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND",
    "redis://authenticate-redis-broker:6379/1",
)


# ---------------------------------------------------------
# Email / Postmark
# ---------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


POSTMARK_SMTP_TOKEN = (
    os.getenv("POSTMARK_SMTP_TOKEN") or os.getenv("POSTMARK_SERVER_API_TOKEN") or ""
).strip()


EMAIL_HOST = os.getenv(
    "EMAIL_HOST",
    "smtp.postmarkapp.com",
)


EMAIL_PORT = int(
    os.getenv(
        "EMAIL_PORT",
        "587",
    )
)


EMAIL_HOST_USER = (
    os.getenv("EMAIL_HOST_USER") or POSTMARK_SMTP_TOKEN or ""
).strip() or None


EMAIL_HOST_PASSWORD = (
    os.getenv("EMAIL_HOST_PASSWORD") or POSTMARK_SMTP_TOKEN or ""
).strip() or None


EMAIL_USE_TLS = env_bool(
    "EMAIL_USE_TLS",
    True,
)


EMAIL_USE_SSL = env_bool(
    "EMAIL_USE_SSL",
    False,
)


if EMAIL_USE_TLS and EMAIL_USE_SSL:
    raise ValueError(
        "EMAIL_USE_TLS et EMAIL_USE_SSL ne peuvent pas être activés en même temps."
    )


DEFAULT_FROM_EMAIL = os.getenv("POSTMARK_FROM_EMAIL")


SERVER_EMAIL = DEFAULT_FROM_EMAIL


EMAIL_TIMEOUT = int(
    os.getenv(
        "EMAIL_TIMEOUT",
        "40",
    )
)


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")


# ---------------------------------------------------------
# Logs
# ---------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": [
            "console",
        ],
        "level": "INFO",
    },
}


# ---------------------------------------------------------
# HTTPS / Reverse proxy
# ---------------------------------------------------------

SECURE_SSL_REDIRECT = env_bool(
    "DJANGO_SECURE_SSL_REDIRECT",
    False,
)


# Nginx transmet :
# X-Forwarded-Proto: https
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


USE_X_FORWARDED_HOST = True


if SECURE_SSL_REDIRECT:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# ---------------------------------------------------------
# CSRF
# ---------------------------------------------------------

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "",
    ).split(",")
    if origin.strip()
]
