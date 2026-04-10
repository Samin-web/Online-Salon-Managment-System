import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print("--- User Status Check ---")
for u in User.objects.all():
    print(f"Username: {u.username}, Email: {u.email}, Is Active: {u.is_active}, Has Password: {u.has_usable_password()}")
