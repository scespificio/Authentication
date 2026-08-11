# Documentation Authenticate_be

Ce document décrit le code present dans `Authenticate_be`. Il couvre l'architecture, les apps Django, les points d'entree API, les taches Celery, et les fichiers d'infra (Docker).

# Organisation du projet / Arborescence utile

==============================

------------

```
Authenticate_be/
│
├── Authenticate/
│   └── config/           <- configuration Django (settings, urls, wsgi/asgi, celery).
│   └── core/             <- gestion des profils & domaines, services.
│       └── migrations/
│       └── services/
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

- Projet Django REST (DRF) avec authentification JWT (Djoser) paramétrable via l'application Django packagée `users`.
- Transmission et vérification de JWT entre sites grâce à des cookies.
- Base de donnees MySQL, cache/broker Redis, emails SMTP, taches async via Celery.
- Deux apps locales principales: `core` et `images`.
- App `tags` externe (fournie par le wheel `django_tags_app-0.1.0-py3-none-any.whl`) utilisee via `tags.models.TaggedItem` et `tags.admin.TagsInline`.
- App `users` externe (fournie par le wheel `django_users_apps-0.1.0-py3-none-any.whl`) utilisee via `users.models.User`, `users.serializers`, `users.views`, `users.emails` et `users.urls`.

## Configuration Django (Authenticate)

Fichier: `Authenticate/config/settings.py`

- DRF: JWT obligatoire par defaut, renderer JSON en prod.
- Djoser: activation + reset password custom via `users.emails`.
- Static: `STATIC_ROOT=staticfiles` et `STATICFILES_STORAGE=whitenoise`.
- Media: `MEDIA_URL=/uploads/`, `MEDIA_ROOT=Authenticate/uploads`.
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

URLConf actif (celui reference dans settings): `Authenticate/config/urls.py`

Routes principales:

- Admin: `/admin/`
- core API, domain authorization, JWT check (custom): `/core/` (voir `Authenticate/core/urls.py`)
- djoser authentication, JWT creation (custom) : 
  - `/users/auth/`
- Debug toolbar: `/__debug__/` (en dev)
- Media: expose en dev via `static()` si `DEBUG=True`

Endpoints core (`Authenticate/core/urls.py`):

```
core/
│
├── home/
│
├── theme/
│   └── me/
│
├── profil/
│   └── me/
│
├── domaine/
│   └── me/
│
└── auth/
    └── authorize/
    └── jwt/
        └── check/
```

Endpoint custom API users :

```
users/
└──  auth/
    └── activation/
    └── resend_activation/
    └── jwt/
          └── create/
```

### Services (`Authenticate/core/services.py`)

- `user_has_domain_access` : Vérifie si l'utilisateur a accès au domaine.

### Models (`Authenticate/core/models.py`)

- `ProfilUtilisateur`: . Champs:  `nom`, `utilisateur` (FK vers `User`), `domaines` (FK ManyToMany vers `Domaine`)
- `Domaine`: Champs: `nom`, `url`.

### Serializers (`Authenticate/core/serializers.py`)

- `DomainSerializer`: informations de base sur le domaine.
- `ProfileSerializer`: informations de base sur le profil utilisateur.

### Views (`Authenticate/core/views.py`)

- `ProfileView`: renvoie les informations sur les profils utilisateurs.
- `ProfileViewDetail`: renvoie les informations sur les profils utilisateur associés à l'utilisateur actuellement connecté.
- `DomainView`: renvoie les informations sur les domaines
- `DomainUserView`: renvoie les informations sur les domaines pour lesquels l'utilisateur est accrédité.
- `AuthorizeView`: vérifie que l'utilisateur est autorisé pour le domaine demandé.
- `CheckCookieView`: vérifie que le JWT reçu est valide et appartient à un utilisateur autorisé pour le domaine dont provient la demande.

### Admin (`Authenticate/core/admin.py`)

- Admin `ProfilUtilisateur`
- Admin `Domaine`

## App `users`

### Models (`Authenticate/users/models.py`)

- `User`: remplace `username` par `email` (auth). Champs: `is_staff`, `is_superuser`
- `EmailTemplate`: modèle d'email (title, content, footer, description).

### Serializers (`Authenticate/users/serializers.py`)

- `UserCreateSerializer`, `UserSerializer`: base Djoser adaptee a l'email 
- `CustomTokenObtainPairSerializer`: login JWT qui renvoie le users et les tokens : contourne la fonction django validate() ; utilise `USERS_LOGIN_FIELD` pour déterminer le champ utilisateur. Quand `USERS_LOGIN_FIELD = "both"`, cherche une correspondence sur les deux champs `username` et `email`.

### Views (`Authenticate/users/views.py`)

- `CustomTokenObtainPairView`: endpoint JWT custom : implémente manuellement le throttling et dépend de `DEFAULT_THROTTLE_RATES`.
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

**N'est pas utilisée actuellement.**

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
- `docker_resources/Authenticate_dc.prod.yml`: services MySQL, Redis, SMTP, backend, worker.
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

- Fichiers `tests.py` existent dans `core` et `images` mais contiennent uniquement des squelettes (pas de tests definis).
- Fichier `init_data.py` existe dans `Authenticate` pour directement créer des données test lors de l'initialisation du projet // A SUPPRIMER OU MODIFIER PAR SECURITE 
