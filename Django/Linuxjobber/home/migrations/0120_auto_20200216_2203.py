# Generated by Django 2.0.7 on 2020-02-16 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0119_auto_20200216_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperienceeligibility',
            name='apt_number',
            field=models.TextField(blank=True, null=True),
        ),
    ]