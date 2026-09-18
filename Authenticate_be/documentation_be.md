# Documentation Authenticate_be

Ce document décrit le code present dans `Authenticate_be`. Il couvre l'architecture, les apps Django, les points d'entree API, les taches Celery, et les fichiers d'infra (Docker).

# Organisation du projet / Arborescence utile

==============================

------------

```
Authenticate_be/
│
├── src/
│   └── theme/           <- configuration Django (settings, urls, wsgi/asgi, celery).
│   └── core/             <- gestion de la config du site.
│       └── migrations/
│       └── templates/
│   └── images/           <- gestion des images, admin, upload en lot. // temporaire
│       └── migrations/
│       └── static/
│       └── templates/
│
└── docker_resources/     <- infra locale/prod. / build images
    └── `Dockerfile.dev`
    └── `Dockerfile.prod`
    └── `docker-compose.prod.yml`
    └── `docker-compose.dev.yml`
```

------------------------

## Vue d'ensemble

- Projet Django REST (DRF) avec authentification manuelle JWT (Djoser) et SSO, transmission et vérification de JWT entre sites grâce à des cookies. paramétrable via l'application Django packagée `users`.
- Base de donnees MySQL, cache/broker Redis, emails SMTP, taches async via Celery.
- Deux apps locales principales: `core` et `images`.
- App `tags` externe (fournie par le wheel `django_tags_app-0.1.0-py3-none-any.whl`) utilisee via `tags.models.TaggedItem` et `tags.admin.TagsInline`.
- App `users` externe (fournie par le wheel `django_users_apps-0.1.3-py3-none-any.whl`) pour le login manuel/SSO et la gestion d'accès aux domaines via cookies de session.

## Configuration Django (Authenticate)

Fichier: `src/config/settings.py`

- DRF: JWT obligatoire par defaut, renderer JSON en prod.
- Djoser: activation + reset password custom via `users.emails`.
- Static: `STATIC_ROOT=staticfiles` et `STATICFILES_STORAGE=whitenoise`.
- Media: `MEDIA_URL=/uploads/`, `MEDIA_ROOT=src/uploads`.
- Celery: `CELERY_BROKER_URL` (Redis) et `CELERY_RESULT_BACKEND`.
- Logging standard console.
- Sécurité: `SECURE_SSL_REDIRECT`, `SECURE_PROXY_SSL_HEADER`, `CSRF_TRUSTED_ORIGINS`.

Variables d'environnement (principales):

- Authentification :  `AUTH_USER_MODEL = "users.User"`, `USERS_LOGIN_FIELD = "username" | "email" | "both"` (authentification sur le champ email par défaut.)
- Django: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_TIME_ZONE`, `DJANGO_ALLOWED_HOSTS`
- CORS: `CORS_ALLOWED_ORIGINS`, `CORS_ALLOW_HEADERS` (ajoute le header custom `X-Requested-Host` pour l'autorisation d'accès à un domaine), `CORS_ALLOW_CREDENTIALS` (permet la création de cookies)
- REST_FRAMEWORK : `DEFAULT_THROTTLE_RATES` (rate limiting : nombre de tentatives de login possibles par minute pour un utilisateur.)
- DB: `DB_NAME`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`
- Email: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`, `EMAIL_TIMEOUT`
- Config : `CONFIG_FILE_FOLDER`, `CONFIG_FILE_NAME`
- Front: `FRONTEND_BASE_URL`, `FRONTEND_DOMAIN`, `FRONTEND_PROTOCOL`
- JWT: `ACCESS_TOKEN_LIFETIME`, `REFRESH_TOKEN_LIFETIME`
- Celery: `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- Sécurité: `DJANGO_SECURE_SSL_REDIRECT`, `CSRF_TRUSTED_ORIGINS`

## URLs et endpoints

URLConf actif (celui reference dans settings): `src/config/urls.py`

Routes principales:

- Admin: `/admin/`
- core API, domain authorization, JWT check (custom): `/core/` (voir `src/core/urls.py`)
- Debug toolbar: `/__debug__/` (en dev)
- Media: expose en dev via `static()` si `DEBUG=True`

Endpoints core (`src/core/urls.py`):

```
core/
│
├── home/
│
└── theme/
    └── me/
```

Endpoints API users :

```
users/
└──  auth/
    └── authorize/
    └── activation/
    └── resend_activation/
    └── jwt/
          └── create/
          └── check/
├── profil/
│   └── me/
│
├── domaine/
│   └── me/
│
└── oidc/
```

## App `images`

**N'est pas utilisée actuellement.**

### Models (`src/images/models.py`)

- `Image`: fichier image et tags (GenericRelation via `TaggedItem`).
- `ImageItem`: associe une image a n'importe quel objet (GenericForeignKey), avec `display_order`.

### Serializers (`src/images/serializers.py`)

- `ImageSerializer`: meta simple.
- `ImageItemSerializer`: expose image en lecture et image_id en ecriture.

### Admin et upload en lot

- `src/images/admin.py`
  - `ImageAdmin`: liste avec preview, tags, et import en lot.
  - `batch_upload_view`: page custom pour importer plusieurs images.
- Formulaires:
  - `src/images/forms.py`: `BatchImageUploadForm` + gestion multi-fichiers.
  - `src/images/widgets.py`: `MultiFileWidget`.
- JS admin:
  - `src/images/static/image/image_title_autofill.js`: autofill du titre a partir du nom de fichier.
- Template admin:
  - `src/images/templates/admin/images/image/batch_upload.html`

## Celery

Fichier: `src/config/celery.py`

- Initialise Celery avec `DJANGO_SETTINGS_MODULE=config.settings`.
- Autodiscover des taches (`users.tasks`).
- Logs de diagnostic au demarrage (broker, backend, mode eager).

## Docker et execution

Fichiers principaux:

- `docker_resources/Dockerfile.dev` / `docker_resources/Dockerfile.prod`: builds Django + dependencies.
- `docker_resources/Authenticate_dc.prod.yml`: services MySQL, Redis, SMTP, backend, worker.
- `nginx-media.conf`: expose `/uploads` via Nginx (port 871 en prod).
- `prodentrypoint.sh`: entrypoint prod.

Ports connus (README): 

- Dev: `5190`
- Prod: `PORT_PROD`
- Media (nginx prod): `PORT_MEDIAS`

## Points d'entree

- `src/manage.py`: CLI Django.
- `src/config/asgi.py` et `src/config/wsgi.py`: serveurs ASGI/WSGI.

## Tests

- Fichiers `tests.py` existent dans `core` et `images` mais contiennent uniquement des squelettes (pas de tests definis).
- Fichier `init_data.py` existe dans `Authenticate` pour directement créer des données test lors de l'initialisation du projet // A SUPPRIMER OU MODIFIER PAR SECURITE 
