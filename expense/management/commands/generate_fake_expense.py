from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth.models import User
from ...models import Category, Expense
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate Fake Expense'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('total', type=int, help='Indicates number of fake expense')

    def handle(self, *args: Any, **options: Any) -> str | None:
        total = options['total']
        users = User.objects.get(id=1)
        categories = Category.objects.all()
        fake = Faker()
        for _ in range(total):
            amount = round(random.uniform(10, 1000), 2)
            date = fake.date_this_year()
            description = fake.sentence()
            user = users
            category = random.choice(categories)

            Expense.objects.create(
                user=user,
                amount=amount,
                date=date,
                description=description,
                category=category
            )
        print('compldted')
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {total} fake expenses'))
