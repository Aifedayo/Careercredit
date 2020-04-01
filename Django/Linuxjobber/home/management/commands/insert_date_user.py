from  users.models import CustomUser
from django.core.management import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        user = CustomUser(
            username='DATE-INFO',
            email='dateinfo@mail.com',
            first_name='DATE',
            last_name='INFO'
        )
        user.set_password('8iu7*IU&')
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                'Date user successfully seeded'
            )
        )