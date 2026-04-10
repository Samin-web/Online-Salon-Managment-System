import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.salons.models import Salon

print("--- Fixing Salon Media Paths ---")
for s in Salon.objects.all():
    updated = False
    if s.license_document and s.license_document.name.startswith('salon/'):
        print(f"Fixing License for {s.name}: {s.license_document.name}")
        s.license_document.name = s.license_document.name.replace('salon/', '', 1)
        updated = True
    
    if s.owner_id_proof and s.owner_id_proof.name.startswith('salon/'):
        print(f"Fixing ID Proof for {s.name}: {s.owner_id_proof.name}")
        s.owner_id_proof.name = s.owner_id_proof.name.replace('salon/', '', 1)
        updated = True

    if s.logo and s.logo.name.startswith('salon/'):
        print(f"Fixing Logo for {s.name}: {s.logo.name}")
        s.logo.name = s.logo.name.replace('salon/', '', 1)
        updated = True

    if s.cover_banner and s.cover_banner.name.startswith('salon/'):
        print(f"Fixing Banner for {s.name}: {s.cover_banner.name}")
        s.cover_banner.name = s.cover_banner.name.replace('salon/', '', 1)
        updated = True

    if updated:
        s.save()
        print(f"Successfully updated {s.name}")

print("\n--- Done ---")
