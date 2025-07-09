# your_app/management/commands/generate_products.py
import random

from faker import Faker
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import Product

fake = Faker()

class Command(BaseCommand):
    help = "Generate sample products"

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Number of products to create')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        created = 0
        
        User.objects.create_user(
            username = settings.ADMIN_USERNAME, email=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD
        )

        for _ in range(total):
            name = fake.unique.word().capitalize()
            description = fake.paragraph(nb_sentences=3)
            original_price = round(random.uniform(100, 1000), 2)
            discount = random.uniform(0.05, 0.3)
            selling_price = round(original_price * (1 - discount), 2)
            inventory_count = random.randint(0, 100)

            Product.objects.create(
                name=name,
                description=description,
                original_price=original_price,
                selling_price=selling_price,
                inventory_count=inventory_count,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully created {created} products."))
