# Generated by Django 2.0.1 on 2018-11-27 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0003_remove_coursedescription_syllabus_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedescription',
            name='syllabus_topic',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
    ]
