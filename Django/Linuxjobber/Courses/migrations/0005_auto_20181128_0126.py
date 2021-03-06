# Generated by Django 2.0.1 on 2018-11-28 00:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Courses', '0004_coursedescription_syllabus_topic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Detail', models.TextField()),
                ('Topic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Courses.CourseTopic')),
            ],
        ),
        migrations.CreateModel(
            name='NoteComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Comment', models.CharField(max_length=200)),
                ('Note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Courses.Note')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='coursedescription',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Courses.Course'),
        ),
    ]
