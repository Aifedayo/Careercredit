# Generated by Django 2.0.7 on 2020-05-07 13:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0139_careercredit'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BillingHistory',
            new_name='PaymentHistory',
        ),
    ]
