# Generated by Django 3.2.21 on 2023-10-23 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='surname',
        ),
    ]
