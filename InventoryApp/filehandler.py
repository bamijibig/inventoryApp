import csv
from django.core.exceptions import ValidationError
from .models import Product, Supplier

def process_csv(file):
    try:
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        created_count = 0

        for row in reader:
            supplier, _ = Supplier.objects.get_or_create(name=row['supplier'])
            Product.objects.create(
                name=row['name'],
                description=row['description'],
                price=row['price'],
                supplier=supplier,
            )
            created_count += 1

        return {"created": created_count, "errors": None}
    except Exception as e:
        return {"created": 0, "errors": str(e)}
