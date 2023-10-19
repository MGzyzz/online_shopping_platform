# Generated by Django 3.2.21 on 2023-10-19 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_rename_shop_id_product_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.category', verbose_name='Категория'),
        ),
    ]
