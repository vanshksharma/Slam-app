# Generated by Django 4.2.2 on 2023-07-10 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0004_project_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(null=True),
        ),
    ]