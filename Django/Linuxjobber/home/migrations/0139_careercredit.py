# Generated by Django 2.0.7 on 2020-05-05 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0138_auto_20200426_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Careercredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=200)),
                ('first_name', models.CharField(max_length=200)),
                ('other_name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('school', models.CharField(max_length=200)),
                ('degree_type', models.CharField(max_length=200)),
                ('course_of_study', models.CharField(max_length=200)),
                ('graduating_year', models.CharField(max_length=200)),
                ('first_classmate_fullname', models.CharField(max_length=200)),
                ('first_classmate_email', models.CharField(max_length=200)),
                ('second_classmate_fullname', models.CharField(max_length=200)),
                ('second_classmate_email', models.CharField(max_length=200)),
                ('lecturer_fullname', models.CharField(max_length=200)),
                ('lecturer_email', models.CharField(max_length=200)),
            ],
        ),
    ]
