# Generated by Django 3.2.15 on 2022-08-23 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='dismissed_setup_wizard',
            field=models.BooleanField(default=False),
        ),
    ]
