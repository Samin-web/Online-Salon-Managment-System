import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.accounts.models import Profile

User = get_user_model()

print("--- Superusers ---")
superusers = User.objects.filter(is_superuser=True)
for u in superusers:
    print(f"Username: {u.username}, Email: {u.email}")

print("\n--- Admin Role Users ---")
admin_profiles = Profile.objects.filter(role='admin')
for p in admin_profiles:
    u = p.user
    print(f"Username: {u.username}, Email: {u.email} (Superuser: {u.is_superuser})")

if not superusers.exists() and not admin_profiles.exists():
    print("\nNo admin users found.")
