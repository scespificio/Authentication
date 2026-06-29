from django.contrib import admin
from core.models import ProfilUtilisateur, Domaine

@admin.register(ProfilUtilisateur)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["nom"]
    ordering = ["-id"]

class ProfilUtilisateurDomaineInline(admin.TabularInline):
    model = ProfilUtilisateur.domaines.through
    extra = 1

    fields = ['domaines']

@admin.register(Domaine)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("nom", "url")
    ordering = ["-id"]