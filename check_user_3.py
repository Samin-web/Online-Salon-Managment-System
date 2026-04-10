import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.salons.models import Salon

User = get_user_model()
try:
    user = User.objects.get(id=3)
    print(f"User found: {user.username}")
    salons = Salon.objects.filter(owner=user)
    print(f"Salons owned by user: {salons.count()}")
    for s in salons:
        print(f"  Salon: {s.name} (ID: {s.id})")
except User.DoesNotExist:
    print("User with ID 3 does not exist.")
except Exception as e:
    print(f"Error: {e}")
