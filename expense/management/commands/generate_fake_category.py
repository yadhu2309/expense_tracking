from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth.models import User
from ...models import Category, Expense
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate Fake Category'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('total', type=int, help='Indicates number of fake category')

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            total = options['total']
            users = User.objects.get(id=1)
            fake = Faker()
            for _ in range(total):
                category = fake.word()
                user = users

                Category.objects.create(
                    user=user,
                    name=category
                )
            print('compldted')
            self.stdout.write(self.style.SUCCESS(f'Successfully generated {total} fake expenses'))
        except Exception as e:
            print(e)
