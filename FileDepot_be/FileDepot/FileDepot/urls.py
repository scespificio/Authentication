"""
URL configuration for FileDepot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, path, include
import debug_toolbar
import djoser
from django.conf import settings
from django.conf.urls.static import static
from core.views import ActivationView, ActivationResendView
from django.views.generic import TemplateView


admin.site.site_header = 'FileDepot'
admin.site.index_title = 'Administration'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

    # --- Tes overrides D'ABORD ---
    path("auth/users/activation/", ActivationView.as_view(), name="activation-custom"),
    path("auth/users/resend_activation/", ActivationResendView.as_view(), name="resend-activation-custom"),

    # --- Ensuite Djoser ---
    path('auth/', include(('djoser.urls', 'djoser'), namespace='djoser')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),  # évite re_path ici, garde path pour la cohérence
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)