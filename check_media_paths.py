import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.salons.models import Salon
from apps.accounts.models import CustomUser

print("--- Salon Paths in DB ---")
for s in Salon.objects.all():
    print(f"Salon: {s.name}")
    print(f"  Logo: {s.logo.name if s.logo else 'None'}")
    print(f"  Banner: {s.cover_banner.name if s.cover_banner else 'None'}")
    print(f"  License: {s.license_document.name if s.license_document else 'None'}")

print("\n--- User Paths in DB ---")
for u in CustomUser.objects.all():
    if u.profile_photo:
        print(f"User: {u.username}, Photo: {u.profile_photo.name}")
