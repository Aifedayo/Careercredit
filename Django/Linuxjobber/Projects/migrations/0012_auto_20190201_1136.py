# Generated by Django 2.0.7 on 2019-02-01 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0011_auto_20190201_0056'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTopicNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='projectcoursetopic',
            name='has_labs',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=1),
        ),
        migrations.AddField(
            model_name='projectcoursetopic',
            name='has_notes',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=1),
        ),
        migrations.AddField(
            model_name='coursetopicnote',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.ProjectCourseTopic'),
        ),
    ]