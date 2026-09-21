<<<<<<< HEAD
from django.urls import path  # noqa: EXE002
from rest_framework import routers
=======
from django.urls import path
>>>>>>> origin/SSO

from . import views

app_name = "core"

<<<<<<< HEAD
router = routers.DefaultRouter()
router.register(r"theme", views.ConfigDetailView, basename="theme")

urlpatterns = [
    path("profil/", views.ProfileView.as_view(), name="profil"),
    path("profil/me/", views.ProfileViewDetail.as_view(), name="profil-me"),
    path("domaine/", views.DomainView.as_view(), name="domaine"),
    path("domaine/me/", views.DomainUserView.as_view(), name="domaine-me"),
    path("auth/authorize/", views.AuthorizeView.as_view(), name="autorisation"),
    path("auth/jwt/check/", views.CheckCookieView.as_view(), name="check-jwt-cookie"),
] + router.urls
=======
urlpatterns = [
    path("theme/", views.ConfigDetailView.as_view({"get": "me"})),
]
>>>>>>> origin/SSO
