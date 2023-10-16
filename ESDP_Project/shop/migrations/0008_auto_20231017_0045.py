# Generated by Django 3.2.21 on 2023-10-16 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_timediscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='timediscount',
            name='discount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='timediscount',
            name='price_with_discount',
            field=models.PositiveIntegerField(default=100),
            preserve_default=False,
        ),
    ]
