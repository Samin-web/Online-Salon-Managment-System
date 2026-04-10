import os
import django
from django.core import mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print("--- User Email Check ---")
for u in User.objects.all():
    print(f"Username: {u.username}, Email: {u.email}")

print("\n--- Testing Real SMTP Email Backend ---")
from django.conf import settings
try:
    with mail.get_connection() as connection:
        mail.EmailMessage(
            'Test Subject',
            'This is a real test email from Online Stylehub.',
            settings.DEFAULT_FROM_EMAIL,
            ['saminmon10@gmail.com'], # Sending to yourself
            connection=connection,
        ).send()
    print("SUCCESS: Real email sent. Please check your inbox.")
except Exception as e:
    print(f"FAILED to send real email: {e}")
