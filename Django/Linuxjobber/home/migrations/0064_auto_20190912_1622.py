# Generated by Django 2.0.7 on 2019-09-12 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0063_merge_20190910_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wetask',
            name='task',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
