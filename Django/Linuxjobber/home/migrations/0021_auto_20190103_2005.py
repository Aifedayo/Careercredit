# Generated by Django 2.0.7 on 2019-01-03 20:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20190103_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='wepeoples',
            name='Paystub',
            field=models.ImageField(null=True, upload_to='resume'),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='last_verification',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]