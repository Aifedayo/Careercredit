# Generated by Django 2.0.7 on 2020-02-16 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0123_auto_20200216_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperienceisa',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdfs'),
        ),
    ]
