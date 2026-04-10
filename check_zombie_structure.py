import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

zombie_tables = [
    'salon_salon', 'salon_staff', 'salon_review', 'salon_reviewreply', 
    'salon_complaint', 'salon_blockedcustomer', 'booking_appointment'
]

with connection.cursor() as cursor:
    for table in zombie_tables:
        print(f"\nStructure of {table}:")
        try:
            cursor.execute(f"DESCRIBE {table}")
            for row in cursor.fetchall():
                print(row)
        except Exception as e:
            print(f"Error describing {table}: {e}")
