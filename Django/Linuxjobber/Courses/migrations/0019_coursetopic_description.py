# Generated by Django 2.0.1 on 2018-12-14 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0018_gradesreport_lab'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetopic',
            name='description',
            field=models.TextField(default='nil'),
        ),
    ]
