# Generated by Django 2.1.2 on 2019-01-22 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Projects', '0002_auto_20190122_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseLab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_id', models.IntegerField(unique=True)),
                ('lab_title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CourseLabTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(unique=True)),
                ('task', models.TextField()),
                ('task_note', models.TextField()),
                ('task_comment', models.TextField()),
                ('task_lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.CourseLab')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(unique=True)),
                ('project_title', models.CharField(max_length=100)),
                ('project_description', models.CharField(max_length=500)),
                ('project_image', models.TextField(max_length=500)),
                ('project_bg_image', models.TextField(max_length=500)),
                ('project_contents', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='ProjectCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.IntegerField(unique=True)),
                ('course_title', models.CharField(max_length=100)),
                ('course_description', models.CharField(max_length=500)),
                ('course_objective', models.CharField(max_length=100)),
                ('course_content', models.CharField(max_length=500)),
                ('course_duration', models.CharField(max_length=20)),
                ('course_image', models.TextField(max_length=1000)),
                ('course_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.Project')),
            ],
            options={
                'verbose_name_plural': 'Projects Course',
            },
        ),
        migrations.CreateModel(
            name='ProjectCourseTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_id', models.IntegerField(unique=True)),
                ('topic_title', models.CharField(max_length=200)),
                ('topic_video', models.CharField(max_length=100)),
                ('topic_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.ProjectCourse')),
            ],
            options={
                'verbose_name_plural': 'Projects Course Topic',
            },
        ),
        migrations.AddField(
            model_name='courselab',
            name='lab_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.ProjectCourse'),
        ),
    ]
