# Generated by Django 4.2.2 on 2023-07-04 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0003_alter_proposal_amount_alter_proposal_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='rate',
            field=models.FloatField(),
        ),
    ]