import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.salons.models.salon import Salon

print("--- Salon Payment Settings ---")
for salon in Salon.objects.all():
    print(f"Salon: {salon.name}")
    print(f"  ID: {salon.id}")
    print(f"  QR Enabled: {salon.is_qr_payment_enabled}")
    print(f"  QR Code: {salon.qr_code}")
    if salon.qr_code:
        try:
            print(f"  QR URL: {salon.qr_code.url}")
        except ValueError as e:
            print(f"  QR URL error: {e}")
    print("-" * 30)
