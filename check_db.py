from django.conf import settings
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.salons.models import Salon, SalonService, Staff, Receptionist
from django.contrib.auth import get_user_model
User = get_user_model()

def check_data():
    print("--- Database Check ---")
    salons = Salon.objects.all()
    print(f"Total Salons: {salons.count()}")
    for s in salons:
        print(f"Salon: {s.name} (ID: {s.id})")
        services = s.services.all()
        active_services = s.services.filter(is_active=True)
        print(f"  Total Services: {services.count()}")
        print(f"  Active Services: {active_services.count()}")
        staff = s.staff.all()
        available_staff = s.staff.filter(is_available=True)
        print(f"  Total Staff: {staff.count()}")
        print(f"  Available Staff: {available_staff.count()}")
        receptionists = s.receptionists.all()
        print(f"  Receptionists: {receptionists.count()}")
        for r in receptionists:
            print(f"    Rec: {r.name} (User: {r.user.username})")

if __name__ == "__main__":
    check_data()
