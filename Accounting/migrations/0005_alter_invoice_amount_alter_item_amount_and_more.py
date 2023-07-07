# Generated by Django 4.2.2 on 2023-07-04 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0004_alter_item_amount_alter_item_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]