# Generated by Django 2.0.7 on 2019-02-16 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_auto_20190216_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='wetask',
            name='group',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]