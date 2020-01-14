from django.core.management.base import BaseCommand
from classroom.models import Connection

class Command(BaseCommand):

    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        Connection.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            'Connection table successfully cleared')
        )