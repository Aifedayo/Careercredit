# Generated by Django 2.1.2 on 2019-01-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0005_userslabtaskstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='userslabtaskstatus',
            name='status_id',
            field=models.CharField(default='default', max_length=20),
        ),
    ]
