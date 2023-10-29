from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Добавляем админа"""
        user = User.objects.create(
            email='egor_manuilov@mail.ru',
            first_name='Egor',
            last_name='Manuilov',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('qwerty')
        user.save()