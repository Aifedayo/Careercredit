# Generated by Django 2.0.7 on 2019-01-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20190103_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wepeoples',
            name='last_verification',
            field=models.ImageField(upload_to='resume'),
        ),
    ]
