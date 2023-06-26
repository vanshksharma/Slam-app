# Generated by Django 4.2.2 on 2023-06-26 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calender', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.AddField(
            model_name='event',
            name='due_date',
            field=models.DateField(default='2023-06-26'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.DateField(default='2023-06-26'),
            preserve_default=False,
        ),
    ]