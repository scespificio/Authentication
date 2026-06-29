#!/usr/bin/env python
import os
import django

# Setup Django FIRST, before any model imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Only import models AFTER django.setup()
from django.contrib.auth import get_user_model
from core.models import ProfilUtilisateur, Domaine
from users.models import User

User = get_user_model()

def create_superuser():
    if User.objects.filter(email='admin@espificio.com').exists():
        print("Superuser already exists")
        return User.objects.get(email='admin@espificio.com')
    
    superuser = User.objects.create_superuser(
        username='admin',
        email='admin@espificio.com',
        password='espificio',
        first_name='Admin',
        last_name='User'
    )
    
    print(f"Created superuser: {superuser.email}")
    return superuser

def create_domains():    
    domain, _ = Domaine.objects.get_or_create(
        nom='CRAOnline',
        url='craonline.espificio.com'
    ) 

    if Domaine.objects.filter(nom='CRAOnline').exists():
        print("Domain already exists.")
    else:
         print("Created domain ", domain.url)

    return domain

def create_profile(superuser, domain):
    if ProfilUtilisateur.objects.filter(nom='admin').exists():
        print("Profile already exists.")
        return

    profile, _ = ProfilUtilisateur.objects.get_or_create(
        utilisateur = superuser,
        nom='admin'
    )

    profile.domaines.add(domain)

    print("Created profile ", profile.nom)

def main():
    print("Creating basic user account...")
    try:
        superuser = create_superuser()
        domain = create_domains()
        create_profile(superuser, domain)

        print("\nDone! Login credentials:")
        print("Email: admin@espificio.com")
        print("Password: espificio")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

main()