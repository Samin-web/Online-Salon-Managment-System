import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_NAME = 'salons_salon' AND TABLE_SCHEMA = DATABASE()")
    constraints = cursor.fetchall()
    print('Foreign key constraints referencing salons_salon:')
    for constraint in constraints:
        print(f'  {constraint[0]}.{constraint[1]} -> {constraint[3]}.{constraint[4]} (constraint: {constraint[2]})')