# Documentation FileDepot_be

Ce document décrit le code present dans `FileDepot_be`. Il couvre l'architecture, les apps Django, les points d'entree API, les taches Celery, et les fichiers d'infra (Docker).

## Vue d'ensemble

- Projet Django REST (DRF) avec authentification JWT (SimpleJWT) et Djoser.
- Base de donnees MySQL, cache/broker Redis, emails SMTP, taches async via Celery.
- Deux apps locales principales: `core` et `images`.
- App `tags` externe (fournie par le wheel `django_tags_app-0.1.0-py3-none-any.whl`) utilisee via `tags.models.TaggedItem` et `tags.admin.TagsInline`.

## Arborescence utile

- `FileDepot/FileDepot/` : configuration Django (settings, urls, wsgi/asgi, celery).
- `FileDepot/core/` : coeur metier (utilisateurs, config, email).
- `FileDepot/images/` : gestion des images, admin, upload en lot.
- `docker_resources/docker-compose.dev.yml` / `docker_resources/docker-compose.prod.yml` : infra locale/prod.
- `docker_resources/Dockerfile.dev` / `docker_resources/Dockerfile.prod` : build images.

## Configuration Django (FileDepot)

Fichier: `FileDepot/FileDepot/settings.py`

- `AUTH_USER_MODEL = "core.User"` (auth via email).
- DRF: JWT obligatoire par defaut, renderer JSON en prod.
- Djoser: activation + reset password custom via `core.emails`.
- Static: `STATIC_ROOT=staticfiles` et `STATICFILES_STORAGE=whitenoise`.
- Media: `MEDIA_URL=/uploads/`, `MEDIA_ROOT=FileDepot/uploads`.
- Celery: `CELERY_BROKER_URL` (Redis) et `CELERY_RESULT_BACKEND`.
- Logging standard console.
- Securite: `SECURE_SSL_REDIRECT`, `SECURE_PROXY_SSL_HEADER`, `CSRF_TRUSTED_ORIGINS`.

Variables d'environnement (principales):

- Django: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_TIME_ZONE`, `DJANGO_ALLOWED_HOSTS`
- CORS: `CORS_ALLOWED_ORIGINS`
- DB: `DB_NAME`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`
- Email: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`, `EMAIL_TIMEOUT`
- Front: `FRONTEND_BASE_URL`, `FRONTEND_DOMAIN`, `FRONTEND_PROTOCOL`
- JWT: `ACCESS_TOKEN_LIFETIME`, `REFRESH_TOKEN_LIFETIME`
- Celery: `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- Sécurité: `DJANGO_SECURE_SSL_REDIRECT`, `CSRF_TRUSTED_ORIGINS`

## URLs et endpoints

URLConf actif (celui reference dans settings): `FileDepot/FileDepot/urls.py`

Routes principales:

- Admin: `/admin/`
- Core API: `/core/` (voir `FileDepot/core/urls.py`)
- Auth Djoser: `/auth/`
- Activation custom:
  - `POST /auth/users/activation/` -> `core.views.ActivationView`
  - `POST /auth/users/resend_activation/` -> `core.views.ActivationResendView`
- Debug toolbar: `/__debug__/` (en dev)
- Media: expose en dev via `static()` si `DEBUG=True`

Endpoints core (`FileDepot/core/urls.py`):

- `GET /core/home/` : ping simple.
- `POST /core/auth/jwt/create` : login JWT custom (renvoie user + tokens).
- `GET /core/config/me/` : config liée a l'utilisateur courant.

### Models (`FileDepot/core/models.py`)

- `User`: remplace `username` par `email` (auth). Champs: `is_staff`, `is_superuser`, `config` (FK vers `WebConfig`).
- `EmailTemplate`: modèle d'email (title, content, footer, description).
- `ChakraTemplate`: JSON de theme UI (champ `chakra`).
- `WebConfig`: profil d'application (logo, emailTemplate, ui_template, config JSON, email commercial, categories, tags).

### Serializers (`FileDepot/core/serializers.py`)

- `UserCreateSerializer`, `UserSerializer`: base Djoser adaptee a l'email.
- `CustomTokenObtainPairSerializer`: login JWT qui renvoie le user et les tokens.
- `WebConfigOutputSerializer`: expose `appName`, `logo`, `email`, `chakra`.

### Views (`FileDepot/core/views.py`)

- `WebConfigDetailView.me`: recupere la config associee a l'utilisateur.
- `CustomTokenObtainPairView`: endpoint JWT custom.
- `ActivationView`: active un compte et envoie un email de reset mot de passe.
- `ActivationResendView`: renvoie un lien d'activation.

### Admin (`FileDepot/core/admin.py`)

- Custom admin pour `User` (login email) + action "Envoyer un e-mail d'activation".
- Admin `WebConfig`: inline Tags (1 max) + logo (ImageItem) + action "Dupliquer".
- Admin `EmailTemplate`, `ChakraTemplate`.

Template admin associe:
- `FileDepot/core/templates/admin/core/product/change_list.html` : toolbar de filtre par categorie.

### Emails et taches

- `FileDepot/core/tasks.py`
  - `send_email`: envoi SMTP HTML via Celery.
  - `send_djoser_email`: reconstruit les emails Djoser dans le worker.
- `FileDepot/core/emails.py`
  - `ActivationEmail` et `PasswordResetEmail`: encapsulent le contexte et deleguent a `send_djoser_email`.
- `FileDepot/core/services/activation.py`
  - `send_activation_email`: action admin pour envoyer un lien d'activation front.
  - `send_password_email`: reset password via template Djoser.
- `FileDepot/core/signals.py`: handlers de signaux Djoser (actuellement commentes).

### Templates email

- `FileDepot/core/templates/email/activation.html`
- `FileDepot/core/templates/email/password_reset.html`

## App `images`

N'est pas utilisée actuellement.

### Models (`FileDepot/images/models.py`)

- `Image`: fichier image et tags (GenericRelation via `TaggedItem`).
- `ImageItem`: associe une image a n'importe quel objet (GenericForeignKey), avec `display_order`.

Les objets `WebConfig` utilisent `ImageItem` via `GenericRelation`.

### Serializers (`FileDepot/images/serializers.py`)

- `ImageSerializer`: meta simple.
- `ImageItemSerializer`: expose image en lecture et image_id en ecriture.

### Admin et upload en lot

- `FileDepot/images/admin.py`
  - `ImageAdmin`: liste avec preview, tags, et import en lot.
  - `batch_upload_view`: page custom pour importer plusieurs images.
- Formulaires:
  - `FileDepot/images/forms.py`: `BatchImageUploadForm` + gestion multi-fichiers.
  - `FileDepot/images/widgets.py`: `MultiFileWidget`.
- JS admin:
  - `FileDepot/images/static/image/image_title_autofill.js`: autofill du titre a partir du nom de fichier.
- Template admin:
  - `FileDepot/images/templates/admin/images/image/batch_upload.html`

## Celery

Fichier: `FileDepot/FileDepot/celery.py`

- Initialise Celery avec `DJANGO_SETTINGS_MODULE=FileDepot.settings`.
- Autodiscover des taches (`core.tasks`).
- Logs de diagnostic au demarrage (broker, backend, mode eager).

## Docker et execution

Fichiers principaux:

- `docker_resources/Dockerfile.dev` / `docker_resources/Dockerfile.prod`: builds Django + dependencies.
- `docker_resources/docker-compose.dev.yml`: services MySQL, Redis, SMTP, backend, worker.
- `docker_resources/docker-compose.prod.yml`: idem + Nginx media en front d'uploads.
- `nginx-media.conf`: expose `/uploads` via Nginx (port 871 en prod).
- `prodentrypoint.sh`: entrypoint prod.

Ports connus (README): 

- Dev: `5180`
- Prod: `PORT_PROD`
- Media (nginx prod): `PORT_MEDIAS`

## Points d'entree

- `FileDepot/manage.py`: CLI Django.
- `FileDepot/FileDepot/asgi.py` et `FileDepot/FileDepot/wsgi.py`: serveurs ASGI/WSGI.

## Tests

- Fichiers `tests.py` existent dans `core` et `images` mais contiennent uniquement des squelettes (pas de tests definis).
- Fichier `init_data.py` existe dans `core` pour directement créer des données test lors de l'initialisation du projet // A SUPPRIMER OU MODIFIER PAR SECURITE 
