from core.models import Domain, UserIAM
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(Group)

admin.site.site_header = (
    f"Gestion des identités et des accès {getattr(settings, 'CUSTOMER_NAME', '')}"
)
admin.site.site_title = f"IAM - {getattr(settings, 'DJANGO_APP_NAME', '')}"
admin.site.index_title = "Administration des identités et des accès"


def get_app_list(request, app_label=None):
    app_list = admin.AdminSite.get_app_list(
        admin.site,
        request,
        app_label,
    )

    app_order = {
        "users": 1,
        "core": 2,
    }

    app_list.sort(
        key=lambda app: app_order.get(
            app["app_label"],
            999,
        )
    )

    return app_list


admin.site.get_app_list = get_app_list


@admin.register(UserIAM)
class UserIAMAdmin(admin.ModelAdmin):
    list_display = ("user_email", "user_username")
    ordering = ("-id",)
    filter_horizontal = ("domaines",)

    @admin.display(description="Email", ordering="user__email")
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description="Utilisateur", ordering="user__username")
    def user_username(self, obj):
        return obj.user.username


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("nom", "url")
    ordering = ("-id",)
    search_fields = ("nom", "url")
