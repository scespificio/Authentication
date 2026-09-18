from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("theme/", views.ConfigDetailView.as_view({"get": "me"})),
]
