# Generated by Django 2.2.2 on 2019-11-24 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0037_coursefeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetopic',
            name='duration',
            field=models.IntegerField(default=5),
        ),
    ]
