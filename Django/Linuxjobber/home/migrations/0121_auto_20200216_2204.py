# Generated by Django 2.0.7 on 2020-02-16 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0120_auto_20200216_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperienceeligibility',
            name='middle_initial',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='workexperienceeligibility',
            name='middle_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]