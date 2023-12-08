# Generated by Django 3.2.21 on 2023-10-27 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_bucket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucket',
            name='session_key',
        ),
        migrations.AddField(
            model_name='bucket',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
