# Generated by Django 2.0.7 on 2020-03-28 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0135_auto_20200328_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wepeoples',
            name='person',
            field=models.CharField(blank=True, choices=[('Trainee', 'Trainee'), ('Student', 'Student')], default='Trainee', max_length=20, null=True),
        ),
    ]
