# Generated by Django 3.2.19 on 2023-05-24 04:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0003_rename_project_payment_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
