import os

# User (authentification)
AUTH_USER_MODEL = "users.User"
USERS_LOGIN_FIELD = os.getenv("USERS_LOGIN_FIELD", "both")
ACTIVATION_MAIL_BODY = os.getenv("USERS_ACTIVATION_MAIL_BODY", "")
USERS_ENABLE_ACTIVATION_EMAIL = (
    os.getenv("USERS_ENABLE_ACTIVATION_EMAIL", "False") == "True"
)
USER_GROUP_DISPLAY = os.getenv("USER_GROUP_DISPLAY", "False") == "True"

# --- Paramètres OIDC ---
USERS_ENABLE_SSO = os.getenv("USERS_ENABLE_SSO", "False") == "True"
OIDC_RP_CLIENT_ID = os.getenv("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_RP_CLIENT_SECRET")

# Front-channel — must be reachable by the browser
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv("OIDC_OP_AUTHORIZATION_ENDPOINT")

# Back-channel — must be reachable by the Django container, on the Docker network
OIDC_OP_TOKEN_ENDPOINT = os.getenv("OIDC_OP_TOKEN_ENDPOINT")
OIDC_OP_USER_ENDPOINT = os.getenv("OIDC_OP_USER_ENDPOINT")
OIDC_OP_JWKS_ENDPOINT = os.environ["OIDC_OP_JWKS_ENDPOINT"]

OIDC_RP_SIGN_ALGO = os.getenv("OIDC_RP_SIGN_ALGO", "RS256")
OIDC_AUTHENTICATION_CALLBACK_URL = os.getenv(
    "OIDC_AUTHENTICATION_CALLBACK_URL", "users:oidc_authentication_callback"
)

OIDC_REDIRECT_ALLOWED_HOSTS = os.getenv("OIDC_REDIRECT_ALLOWED_HOSTS")

LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", "/connexion/")
LOGOUT_REDIRECT_URL = os.getenv("LOGOUT_REDIRECT_URL", "/connexion/")
