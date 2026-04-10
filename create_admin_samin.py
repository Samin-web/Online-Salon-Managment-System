import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.accounts.models import Profile

User = get_user_model()

username = "samin"
password = "samin@123"
email = "samin@stylehub.com"

try:
    if User.objects.filter(username=username).exists():
        print(f"User {username} already exists. Updating role to admin.")
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser {username} created.")

    profile, created = Profile.objects.get_or_create(user=user)
    profile.role = 'admin'
    profile.save()
    print(f"Profile for {username} updated with role: {profile.role}")

except Exception as e:
    print(f"Error: {e}")
