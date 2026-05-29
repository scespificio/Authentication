#!/usr/bin/env python
import os
import django

# Setup Django FIRST, before any model imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FileDepot.settings')
django.setup()

# Only import models AFTER django.setup()
from django.contrib.auth import get_user_model
from core.models import ChakraTemplate, WebConfig, Fichier

User = get_user_model()

def create_default_config():
    ui_template, _ = ChakraTemplate.objects.get_or_create(
        name="Default",
        defaults={"description": "Modèle d'UI par défaut", "chakra": {}}
    )
    config, _ = WebConfig.objects.get_or_create(
        name="Default",
        defaults={"ui_template": ui_template, "config": {}}
    )
    return config

def create_superuser(config):
    if User.objects.filter(email='admin@espificio.com').exists():
        print("Superuser already exists")
        return
    user = User.objects.create_superuser(
        email='admin@espificio.com',
        password='espificio',
        first_name='Admin',
        last_name='User',
        config=config
    )
    print(f"Created superuser: {user.email}")

def assign_config_to_existing_users():
    config = create_default_config()
    updated = User.objects.filter(config__isnull=True).update(config=config)
    print(f"Assigned config to {updated} user(s)")

def create_file_entry():
    if Fichier.objects.filter(nom="Lorem Ipsum").exists():
        print("File already exists")
        return
    file = Fichier.objects.create(
        nom = "Lorem Ipsum",
        chemin = "/path/of/your/file/file.extension"
    )
    print(f"Created file: {file.nom}")

def main():
    print("Creating basic user account...")
    try:
        config = create_default_config()
        create_superuser(config)
        assign_config_to_existing_users()
        create_file_entry()
        print("\nDone! Login credentials:")
        print("Email: admin@espificio.com")
        print("Password: espificio")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

main()