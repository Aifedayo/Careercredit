# Generated by Django 2.0.7 on 2019-12-15 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0103_auto_20191215_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subpayment',
            name='installment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.InstallmentPlan'),
        ),
    ]
