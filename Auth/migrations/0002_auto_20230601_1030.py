# Generated by Django 3.2.19 on 2023-06-01 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
