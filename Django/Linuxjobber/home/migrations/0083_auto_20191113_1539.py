# Generated by Django 2.2.2 on 2019-11-13 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0082_completeclass_completeclasscertificate_completeclasslearn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='completeclasscertificate',
            old_name='name_of_image',
            new_name='url_of_image',
        ),
    ]