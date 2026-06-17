from django.urls import path, include
from rest_framework import routers
from .views import ProfileSerializer, CompanySerializer, DomainSerializer

app_name = 'core'

urlpatterns = [
    path('profil/', ProfileSerializer.as_view(), name='profil'),
    path('société/', CompanySerializer.as_view(), name='société'),
    path('domaine/', DomainSerializer.as_view(), name='domaine')
]
