# Generated by Django 3.2.21 on 2023-10-16 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20231017_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timediscount',
            name='price_with_discount',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
