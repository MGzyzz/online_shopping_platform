# Generated by Django 3.2.21 on 2023-12-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_auto_20231124_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproducts',
            name='price_per_product',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]