# Generated by Django 2.0.7 on 2020-02-13 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0116_auto_20200131_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperienceeligibility',
            name='pdf',
            field=models.FileField(null=True, upload_to='pdfs/'),
        ),
        migrations.AlterField(
            model_name='workexperienceeligibility',
            name='terms',
            field=models.FileField(null=True, upload_to='pdfs/'),
        ),
        migrations.AlterField(
            model_name='workexperienceisa',
            name='pdf',
            field=models.FileField(null=True, upload_to='pdfs'),
        ),
    ]
