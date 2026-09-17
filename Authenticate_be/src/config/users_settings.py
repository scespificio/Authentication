import os

# User (authentification)
AUTH_USER_MODEL = "users.User"
USERS_LOGIN_FIELD = os.getenv("USERS_LOGIN_FIELD", "both")
ACTIVATION_MAIL_BODY = os.getenv("USERS_ACTIVATION_MAIL_BODY", "")
USERS_ENABLE_ACTIVATION_EMAIL = (
    os.getenv("USERS_ENABLE_ACTIVATION_EMAIL", "False") == "True"
)
USER_GROUP_DISPLAY = os.getenv("USER_GROUP_DISPLAY", "False") == "True"
