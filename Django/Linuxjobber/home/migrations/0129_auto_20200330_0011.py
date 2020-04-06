# Generated by Django 2.0.7 on 2020-03-30 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0128_merge_20200321_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkexpFormStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(blank=True, max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='wepeoples',
            name='personn',
            field=models.CharField(choices=[('Trainee', 'Trainee'), ('Student', 'Student')], default='Trainee', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='current_position',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='graduation_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='income',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='last_verification',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='resume'),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='relocation',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='start_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='wepeoples',
            name='types',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.wetype'),
        ),
    ]