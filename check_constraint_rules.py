import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT CONSTRAINT_NAME, DELETE_RULE, UPDATE_RULE FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS WHERE CONSTRAINT_NAME = 'salon_servicecategory_salon_id_a1114242_fk_salon_salon_id'")
    constraint = cursor.fetchone()
    if constraint:
        print(f'Constraint: {constraint[0]}, Delete Rule: {constraint[1]}, Update Rule: {constraint[2]}')
    else:
        print('Constraint not found')