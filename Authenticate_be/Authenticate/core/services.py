from django.db.models import Q
from .models import ProfilUtilisateur, Domaine

def user_has_domain_access(user, host:str) -> tuple[bool, int | None]:
    """
    Vérifie si `user` a accès au domaine `host`.
    Retourne (autorisé: bool, message_erreur: str | None)
    """

    if host[-1] == "/":
        host = host[:-1]  # Supprimer le slash final si présent
    '''host_split_subdomain = host.split("/")[0] 
    host_split_root = host_split_subdomain.split(".")[1:]
    host_suffix = "." + ".".join(host_split_root)''' # DEPRECATED, à utiliser si on doit gérer des domaines autres qu'Espificio.com
    
    domain = Domaine.objects.filter(url=host).first() # Chercher le domaine demandé dans la base de données
    if not domain :
        return False, 404

    has_access = ProfilUtilisateur.objects.filter(Q(utilisateur=user), Q(domaines=domain)).exists() # Chercher si l'utilisateur est accrédité au domaine demandé
    if not has_access :
        return False, 403

    return True, 200
