# Generated by Django 2.1.2 on 2019-01-22 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcourse',
            name='projectgroup',
        ),
        migrations.RemoveField(
            model_name='projectncomment',
            name='project_ng',
        ),
        migrations.RemoveField(
            model_name='projectncomment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='projectnote',
            name='ngroup',
        ),
        migrations.RemoveField(
            model_name='projectnotegroup',
            name='course',
        ),
        migrations.RemoveField(
            model_name='projectnotegroup',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='projecttopic',
            name='project_course',
        ),
        migrations.DeleteModel(
            name='ProjectCourse',
        ),
        migrations.DeleteModel(
            name='ProjectGroup',
        ),
        migrations.DeleteModel(
            name='ProjectNComment',
        ),
        migrations.DeleteModel(
            name='ProjectNote',
        ),
        migrations.DeleteModel(
            name='ProjectNoteGroup',
        ),
        migrations.DeleteModel(
            name='ProjectTopic',
        ),
    ]