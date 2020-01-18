# Generated by Django 2.2.2 on 2019-11-13 12:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0037_coursefeedback'),
        ('home', '0081_auto_20191016_0143'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompleteClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('about', models.TextField()),
                ('prerequisite', models.TextField()),
                ('fee', models.CharField(default='1,225.00', max_length=200)),
                ('pay_url', models.CharField(max_length=200)),
                ('due_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='CompleteClassLearn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('weight', models.IntegerField()),
                ('completeclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.CompleteClass')),
            ],
            options={
                'unique_together': {('weight', 'completeclass')},
            },
        ),
        migrations.CreateModel(
            name='CompleteClassCertificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_image', models.TextField()),
                ('weight', models.IntegerField()),
                ('completeclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.CompleteClass')),
            ],
            options={
                'unique_together': {('weight', 'completeclass')},
            },
        ),
    ]
