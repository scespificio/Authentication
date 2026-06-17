from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'core'

router = routers.DefaultRouter()
router.register(r'theme', views.ConfigDetailView, basename='theme')

urlpatterns = [
    path('profil/', views.ProfileView.as_view(), name='profil'),
    path('profil/me/', views.ProfileViewDetail.as_view(), name='profil-me'),
    path('societe/', views.CompanyView.as_view(), name='société'),
    path('societe/me', views.CompanyViewDetail.as_view(), name='société-me'),
    path('domaine/', views.DomainView.as_view(), name='domaine')
] + router.urls
