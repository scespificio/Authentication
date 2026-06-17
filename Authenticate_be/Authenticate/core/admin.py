from django.contrib import admin
from core.models import Société, Profil, Domaine

@admin.register(Société)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["nom"]
    ordering = ["-id"]

@admin.register(Profil)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["nom"]
    ordering = ["-id"]

@admin.register(Domaine)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("nom", "url")
    ordering = ["-id"]