import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables found: {tables}")
    
    if 'salon_salon' in tables:
        print("\nStructure of salon_salon:")
        cursor.execute("DESCRIBE salon_salon")
        for row in cursor.fetchall():
            print(row)
        
        print("\nRows in salon_salon pointing to ID 3:")
        cursor.execute("SELECT * FROM salon_salon WHERE owner_id = 3")
        rows = cursor.fetchall()
        print(f"Found {len(rows)} rows.")
        for row in rows:
            print(row)
    else:
        print("\n'salon_salon' table not found in current database.")
