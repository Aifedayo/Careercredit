# Generated by Django 2.0.7 on 2019-02-10 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_wework_weight'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wework',
            unique_together={('we_people', 'weight')},
        ),
    ]