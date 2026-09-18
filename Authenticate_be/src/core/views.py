import json
import os

from django.conf import settings
from dotenv import load_dotenv
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

load_dotenv()

CONFIG_FOLDER = os.getenv("CONFIG_FILE_FOLDER")
CONFIG_FILE = os.getenv("CONFIG_FILE_NAME")
DOMAIN_NAME = os.getenv("DOMAIN_NAME")


class ConfigDetailView(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = WebConfigOutputSerializer
    # pas de listing; on garde select_related pour éviter les N+1
    # queryset = WebConfig.objects.select_related("emailTemplate", "ui_template").none()

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        file_path = os.path.join(settings.BASE_DIR, CONFIG_FOLDER, CONFIG_FILE)

        if not os.path.exists(file_path):
            return Response(
                {"error": f"JSON file not found at:{file_path}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return Response(data, status=status.HTTP_200_OK)
