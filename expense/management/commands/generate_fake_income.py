from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth.models import User
from ...models import Category, Expense, Income
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate Fake Income'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('total', type=int, help='Indicates number of fake Income')

    def handle(self, *args: Any, **options: Any) -> str | None:
        total = options['total']
        users = User.objects.get(id=1)
        fake = Faker()
        for _ in range(total):
            amount = round(random.uniform(10, 1000), 2)
            date = fake.date_this_year()
            description = fake.sentence()
            user = users

            Income.objects.create(
                user=user,
                amount=amount,
                date=date,
                description=description,
            )
        print('compldted')
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {total} fake income'))
