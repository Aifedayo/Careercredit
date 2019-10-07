from django.core.management.base import BaseCommand
from home.management.faq_data import get_faqs, \
    get_workexperience_faqs, get_wefaqs_job_section
from home.models import FAQ

class Command(BaseCommand):

    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        # FAQ.truncate()
        FAQ.objects.all().delete()
        self.seed_workexperience_faq()
        self.seed_wefaqs_job_section()
        self.seed_faq()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

    def seed_workexperience_faq(self):
        for faq in get_workexperience_faqs():
            FAQ(
               question=faq['question'],
               response=faq['answer'],
               is_wefaq=True
            ).save()

    def seed_wefaqs_job_section(self):
        for faq in get_wefaqs_job_section():
            FAQ(
               question=faq['question'],
               response=faq['answer'],
               is_wefaq=True,
               is_fifty_percent_faq=True
            ).save()

    def seed_faq(self):
        for faq in get_faqs():
            FAQ(
               question=faq['question'],
               response=faq['answer']
            ).save()