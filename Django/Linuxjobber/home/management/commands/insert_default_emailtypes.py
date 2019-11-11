from django.core.management import BaseCommand

from home.models import EmailMessageType

"""
linuxjobber Default Mail Types

1. no-reply - no-reply
2. Staff mail - Azeem from Linuxjobber
3. Custom - Linuxjobber Career Switch
4. Default - Linuxjobber

:param args:
:param kwargs:
:return:
"""
TYPES = {
    'default': {
        'is_default': True,
        'header_format': "Linuxjobber"
    },
    'custom': {
        'is_default': False,
        'header_format': "{}"
    },
    'staff_mail': {
        'is_default': False,
        'header_format': "{} from Linuxjobber"
    },
    'no-reply': {
        'is_default': False,
        'header_format': "no-reply"
    },

}

# class MailTypes:
#     def __init__(self):
#         for type_name,value in TYPES.items():
#             setattr(self,type_name,"{}".format(type_name))

# def get_mail_types():
#     return MailTypes()

class Command(BaseCommand):

    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        EmailMessageType.objects.all().delete()

        for key,value in TYPES.items():
            EmailMessageType.objects.create(
                type= key,
                header_format=value['header_format'],
                is_default= value['is_default']
            )
            self.stdout.write(self.style.SUCCESS('{} mail type added successfully'.format(
                key
            )))
        self.stdout.write(self.style.SUCCESS('{} mail types added successfully'.format(
            len(TYPES)
        )))



