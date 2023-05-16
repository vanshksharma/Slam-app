# Generated by Django 3.2.19 on 2023-05-16 06:25

import Pipeline.constants
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pipeline', '0002_alter_lead_confidence'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='lead',
            name='Confidence Range Check',
        ),
        migrations.AlterField(
            model_name='lead',
            name='stage',
            field=models.CharField(choices=[('OPPORTUNITY', 'Opportunity'), ('CONTACTED', 'Contacted'), ('NEGOTIATION', 'Negotiation'), ('CLOSED_WON', 'Closed Won'), ('CLOSED_LOST', 'Closed Lost')], default=Pipeline.constants.StageConstant['OPPORTUNITY'], max_length=15),
        ),
    ]
