# Generated by Django 4.2.2 on 2023-06-30 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pipeline', '0003_contact_city_contact_country_contact_phone_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='name',
            field=models.CharField(default='none', max_length=20),
            preserve_default=False,
        ),
    ]
