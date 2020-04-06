# Generated by Django 2.0.7 on 2020-03-01 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0016_connection'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.ChatRoom')),
            ],
        ),
    ]