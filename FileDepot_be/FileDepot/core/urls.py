from django.urls import path, include
from rest_framework import routers
from . import views 
from .views import WebConfigDetailView, CustomTokenObtainPairView, FichierView, FichierDetailView

from . import views 

router = routers.DefaultRouter()
router.register(r'config', WebConfigDetailView, basename='config')

app_name = 'core'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('files/', views.FichierView.as_view(), name='files'),
    path('files/<str:id>/', views.FichierDetailView.as_view(), name='files-detail'),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create')
] + router.urls
