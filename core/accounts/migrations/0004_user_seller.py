# Generated by Django 3.2.21 on 2023-10-13 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='seller',
            field=models.BooleanField(default=False),
        ),
    ]