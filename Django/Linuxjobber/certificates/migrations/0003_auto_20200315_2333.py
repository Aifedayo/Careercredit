# Generated by Django 2.0.7 on 2020-03-15 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0002_auto_20200114_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduatecertificates',
            name='alternate_graduate_image',
            field=models.ImageField(blank=True, null=True, upload_to='certs/'),
        ),
    ]
