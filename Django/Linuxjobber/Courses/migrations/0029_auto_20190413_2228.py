# Generated by Django 2.0.7 on 2019-04-13 22:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0028_auto_20190402_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topicstatus',
            name='video',
        ),
        migrations.AddField(
            model_name='topicstatus',
            name='last_watched',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
