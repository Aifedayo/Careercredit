# Generated by Django 2.0.7 on 2019-09-20 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0064_auto_20190912_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='fulltimepostion',
            name='next_page',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='fulltimepostion',
            name='not_interested_page',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='fulltimepostion',
            name='skilled_page',
            field=models.CharField(default='', max_length=500),
        ),
    ]
