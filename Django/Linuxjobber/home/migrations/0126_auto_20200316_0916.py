# Generated by Django 2.0.7 on 2020-03-16 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0125_auto_20200316_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='wetask',
            name='has_video',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wetask',
            name='video_url',
            field=models.TextField(default='None'),
        ),
    ]