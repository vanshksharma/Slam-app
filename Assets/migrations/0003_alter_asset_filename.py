# Generated by Django 4.2.2 on 2023-07-10 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Assets', '0002_auto_20230622_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='filename',
            field=models.CharField(max_length=100),
        ),
    ]