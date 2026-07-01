from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# User (authentification)
AUTH_USER_MODEL = "users.User"
USERS_LOGIN_FIELD = "both"  # "username", "email" ou "both"
ACTIVATION_MAIL_BODY = """
                <p>Bonjour <strong>{{ user.get_full_name|default:user.email }}</strong>,</p>
              <p>Votre enseigne vous a enregistré sur la plateforme Template son agence de communication.</p>
              <p>Vous y retrouverez l'ensemble des produits et services disponibles pour les magasins de l'enseigne.</p>

              <p>Voici votre lien pour activer votre compte. Il est valide pour 48h :</p>
              <p>Au-delà de ce délai, vous pouvez nous redemander un nouveau lien en nous écrivant à :</p>
              <p>contact@arevagence.com</p>
              """