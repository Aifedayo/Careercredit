# Generated by Django 2.0.1 on 2018-12-17 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0021_auto_20181217_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons'),
        ),
    ]
