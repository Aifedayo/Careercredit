# Generated by Django 2.0.7 on 2019-04-26 19:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Courses', '0033_auto_20190426_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(25)])),
                ('status', models.CharField(default='start_video', max_length=200)),
                ('last_watched', models.DateTimeField(default=django.utils.timezone.now)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Courses.CourseTopic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]