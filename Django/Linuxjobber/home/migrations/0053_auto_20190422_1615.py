# Generated by Django 2.0.7 on 2019-04-22 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0052_wepeoples_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='user',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
