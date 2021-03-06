# Generated by Django 2.0.7 on 2020-04-03 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0130_wework_trainee_stat'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeTraineeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainee_stat', models.CharField(choices=[('Pending', 'Pending'), ('In-progress', 'In-progress'), ('Stopped', 'Stopped'), ('Extended', 'Extended'), ('Ready-state', 'Ready-state'), ('Completed', 'Completed')], default='Pending', max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='wework',
            name='trainee_stat',
        ),
    ]
