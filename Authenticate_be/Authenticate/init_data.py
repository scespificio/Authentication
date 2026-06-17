#!/usr/bin/env python
import os
import django

# Setup Django FIRST, before any model imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Only import models AFTER django.setup()
from django.contrib.auth import get_user_model
from core.models import Profil, Société, Domaine

User = get_user_model()

def create_superuser():
    if User.objects.filter(email='admin@espificio.com').exists():
        print("Superuser already exists")
        return User.objects.get(email='admin@espificio.com')
    
    superuser = User.objects.create_superuser(
        email='admin@espificio.com',
        password='espificio',
        first_name='Admin',
        last_name='User'
    )
    
    print(f"Created superuser: {superuser.email}")
    return superuser

def create_company():
    if Société.objects.filter(nom='Espificio').exists():
        print("Company already exists.")
        return Société.objects.get(nom='Espificio')
    
    company, _ = Société.objects.get_or_create(
        nom='Espificio'
    )

    print("Created company ", company.nom)
    return company

def create_profile(superuser, company):
    if Profil.objects.filter(nom='admin').exists():
        print("Profile already exists.")
        return

    profile, _ = Profil.objects.get_or_create(
        utilisateur = superuser,
        société = company,
        nom='admin'
    )

    print("Created profile ", profile.nom)

def create_domain(company):
    if Domaine.objects.filter(nom='CRAOnline').exists():
        print("Domain already exists.")
        return
    
    domain, _ = Domaine.objects.get_or_create(
        société = company,
        nom='CRAOnline',
        url='craonline.espificio.com'
    ) 

    print("Created domain ", domain.url)

def main():
    print("Creating basic user account...")
    try:
        superuser = create_superuser()
        company = create_company()
        create_profile(superuser, company)
        create_domain(company)

        print("\nDone! Login credentials:")
        print("Email: admin@espificio.com")
        print("Password: espificio")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

main()