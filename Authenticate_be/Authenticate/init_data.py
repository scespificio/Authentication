#!/usr/bin/env python
import os
import django

# Setup Django FIRST, before any model imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Only import models AFTER django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    if User.objects.filter(email='admin@espificio.com').exists():
        print("Superuser already exists")
        return
    user = User.objects.create_superuser(
        email='admin@espificio.com',
        password='espificio',
        first_name='Admin',
        last_name='User'
    )
    print(f"Created superuser: {user.email}")

def main():
    print("Creating basic user account...")
    try:
        create_superuser()
        print("\nDone! Login credentials:")
        print("Email: admin@espificio.com")
        print("Password: espificio")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

main()