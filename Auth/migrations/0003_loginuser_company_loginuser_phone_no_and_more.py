# Generated by Django 4.2.2 on 2023-07-07 17:02

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_auto_20230601_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginuser',
            name='company',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='loginuser',
            name='phone_no',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+912222222226', max_length=128, region=None, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='first_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='last_name',
            field=models.CharField(max_length=20),
        ),
    ]
