# Generated by Django 3.2.21 on 2023-10-21 09:15
import taggit
from django.db import migrations, models
import django.db.models.deletion

from core.settings import LOGO_IMG_UPLOAD_PATH


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0014_rename_shop_id_product_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='logo',
            field=models.ImageField(blank=True, default='def.png', null=True, upload_to=LOGO_IMG_UPLOAD_PATH,
                                    verbose_name='Логотип магазина'),
        ),
        migrations.CreateModel(
            name='TimeDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.PositiveIntegerField(default=0)),
                ('discounted_price', models.PositiveIntegerField(blank=True, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_discount',
                                              to='shop.product')),
            ],
        )
    ]
