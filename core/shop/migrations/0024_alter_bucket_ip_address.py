# Generated by Django 3.2.21 on 2023-10-30 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_alter_bucket_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
    ]
