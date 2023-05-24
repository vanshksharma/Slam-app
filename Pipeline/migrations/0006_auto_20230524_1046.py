# Generated by Django 3.2.19 on 2023-05-24 05:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pipeline', '0005_lead_amount_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='lead',
            name='updated_at',
            field=models.DateField(default=datetime.date.today),
        ),
    ]