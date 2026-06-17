# Documentation Authenticate_be

Ce document décrit le code present dans `Authenticate_be`. Il couvre l'architecture, les apps Django, les points d'entree API, les taches Celery, et les fichiers d'infra (Docker).

## Vue d'ensemble

- Projet Django REST (DRF) avec authentification JWT (SimpleJWT) et Djoser.
- Base de donnees MySQL, cache/broker Redis, emails SMTP, taches async via Celery.
- Deux apps locales principales: `users` et `images`.
- App `tags` externe (fournie par le wheel `django_tags_app-0.1.0-py3-none-any.whl`) utilisee via `tags.models.TaggedItem` et `tags.admin.TagsInline`.

## Arborescence utile

- `Authenticate/config/` : configuration Django (settings, urls, wsgi/asgi, celery).
- `Authenticate/users/` : gestion des utilisateurs (utilisateurs, config, email).
- `Authenticate/images/` : gestion des images, admin, upload en lot.
- `docker_resources/docker-compose.dev.yml` / `docker_resources/docker-compose.prod.yml` : infra locale/prod.
- `docker_resources/Dockerfile.dev` / `docker_resources/Dockerfile.prod` : build images.

## Configuration Django (Authenticate)

Fichier: `Authenticate/config/settings.py`

- `AUTH_USER_MODEL = "users.User"` (auth via email).
- DRF: JWT obligatoire par defaut, renderer JSON en prod.
- Djoser: activation + reset password custom via `users.emails`.
- Static: `STATIC_ROOT=staticfiles` et `STATICFILES_STORAGE=whitenoise`.
- Media: `MEDIA_URL=/uploads/`, `MEDIA_ROOT=Authenticate/uploads`.
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

URLConf actif (celui reference dans settings): `Authenticate/config/urls.py`

Routes principales:

- Admin: `/admin/`
- users API: `/users/` (voir `Authenticate/users/urls.py`)
- Auth Djoser: `/auth/`
- Activation custom:
  - `POST /auth/users/activation/` -> `users.views.ActivationView`
  - `POST /auth/users/resend_activation/` -> `users.views.ActivationResendView`
- Debug toolbar: `/__debug__/` (en dev)
- Media: expose en dev via `static()` si `DEBUG=True`

Endpoints users (`Authenticate/users/urls.py`):

- `GET /users/home/` : ping simple.
- `POST /users/auth/jwt/create` : login JWT custom (renvoie users + tokens).
- `GET /users/config/me/` : config liée a l'utilisateur courant.

### Models (`Authenticate/users/models.py`)

- `User`: remplace `username` par `email` (auth). Champs: `is_staff`, `is_superuser`
- `EmailTemplate`: modèle d'email (title, content, footer, description).

### Serializers (`Authenticate/users/serializers.py`)

- `UserCreateSerializer`, `UserSerializer`: base Djoser adaptee a l'email.
- `CustomTokenObtainPairSerializer`: login JWT qui renvoie le users et les tokens.

### Views (`Authenticate/users/views.py`)

- `CustomTokenObtainPairView`: endpoint JWT custom.
- `ActivationView`: active un compte et envoie un email de reset mot de passe.
- `ActivationResendView`: renvoie un lien d'activation.

### Admin (`Authenticate/users/admin.py`)

- Custom admin pour `User` (login email) + action "Envoyer un e-mail d'activation".
- Admin `EmailTemplate`

Template admin associe:
- `Authenticate/users/templates/admin/users/product/change_list.html` : toolbar de filtre par categorie.

### Emails et taches

- `Authenticate/users/tasks.py`
  - `send_email`: envoi SMTP HTML via Celery.
  - `send_djoser_email`: reconstruit les emails Djoser dans le worker.
- `Authenticate/users/emails.py`
  - `ActivationEmail` et `PasswordResetEmail`: encapsulent le contexte et deleguent a `send_djoser_email`.
- `Authenticate/users/services/activation.py`
  - `send_activation_email`: action admin pour envoyer un lien d'activation front.
  - `send_password_email`: reset password via template Djoser.
- `Authenticate/users/signals.py`: handlers de signaux Djoser (actuellement commentes).

### Templates email

- `Authenticate/users/templates/email/activation.html`
- `Authenticate/users/templates/email/password_reset.html`

## App `images`

N'est pas utilisée actuellement.

### Models (`Authenticate/images/models.py`)

- `Image`: fichier image et tags (GenericRelation via `TaggedItem`).
- `ImageItem`: associe une image a n'importe quel objet (GenericForeignKey), avec `display_order`.

### Serializers (`Authenticate/images/serializers.py`)

- `ImageSerializer`: meta simple.
- `ImageItemSerializer`: expose image en lecture et image_id en ecriture.

### Admin et upload en lot

- `Authenticate/images/admin.py`
  - `ImageAdmin`: liste avec preview, tags, et import en lot.
  - `batch_upload_view`: page custom pour importer plusieurs images.
- Formulaires:
  - `Authenticate/images/forms.py`: `BatchImageUploadForm` + gestion multi-fichiers.
  - `Authenticate/images/widgets.py`: `MultiFileWidget`.
- JS admin:
  - `Authenticate/images/static/image/image_title_autofill.js`: autofill du titre a partir du nom de fichier.
- Template admin:
  - `Authenticate/images/templates/admin/images/image/batch_upload.html`

## Celery

Fichier: `Authenticate/config/celery.py`

- Initialise Celery avec `DJANGO_SETTINGS_MODULE=config.settings`.
- Autodiscover des taches (`users.tasks`).
- Logs de diagnostic au demarrage (broker, backend, mode eager).

## Docker et execution

Fichiers principaux:

- `docker_resources/Dockerfile.dev` / `docker_resources/Dockerfile.prod`: builds Django + dependencies.
- `docker_resources/docker-compose.dev.yml`: services MySQL, Redis, SMTP, backend, worker.
- `docker_resources/docker-compose.prod.yml`: idem + Nginx media en front d'uploads.
- `nginx-media.conf`: expose `/uploads` via Nginx (port 871 en prod).
- `prodentrypoint.sh`: entrypoint prod.

Ports connus (README): 

- Dev: `5190`
- Prod: `PORT_PROD`
- Media (nginx prod): `PORT_MEDIAS`

## Points d'entree

- `Authenticate/manage.py`: CLI Django.
- `Authenticate/config/asgi.py` et `Authenticate/config/wsgi.py`: serveurs ASGI/WSGI.

## Tests

- Fichiers `tests.py` existent dans `users` et `images` mais contiennent uniquement des squelettes (pas de tests definis).
- Fichier `init_data.py` existe dans `Authenticate` pour directement créer des données test lors de l'initialisation du projet // A SUPPRIMER OU MODIFIER PAR SECURITE 
