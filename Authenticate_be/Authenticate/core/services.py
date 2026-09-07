from .models import Domain, UserIAM


def user_has_domain_access(user, host: str) -> tuple[bool, int | None]:
    """
    Vérifie si `user` a accès au domaine `host`.
    Retourne (autorisé: bool, code_statut: int | None)
    """

    if host[-1] == "/":
        host = host[:-1]

    domain = Domain.objects.filter(url=host).first()

    if not domain:
        return False, 404

    has_access = UserIAM.objects.filter(
        user=user,
        domaines=domain,
    ).exists()

    if not has_access:
        return False, 403

    return True, 200
