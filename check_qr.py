import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.salons.models import Salon

salons = Salon.objects.filter(name__icontains='La')
print('Salons with La in name:')
for s in salons:
    print(f'{s.name}: QR={s.qr_code}, URL={s.qr_code.url if s.qr_code else None}, Enabled={s.is_qr_payment_enabled}')