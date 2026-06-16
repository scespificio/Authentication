from django.urls import path, include
from rest_framework import routers
from . import views 
from .views import CustomTokenObtainPairView, ConfigDetailView

from . import views 

router = routers.DefaultRouter()
router.register(r'config', ConfigDetailView, basename='config')

app_name = 'user'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create')
] + router.urls
