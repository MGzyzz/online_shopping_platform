from django.db import models
from django.db.models import TextChoices
from shop.models import ShopModel


class ProductModel(models.Model):
    shop_id = models.ForeignKey(ShopModel, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Название продукта')
    description = models.TextField(max_length=500, null=False, blank=False, verbose_name='Описание')
    vendor_code = models.IntegerField(unique=True, null=False, blank=False, verbose_name='Код Поставщика')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.PositiveIntegerField(default=0, null=False, blank=False, verbose_name='Цена')
    discount = models.PositiveIntegerField(default=0, null=False, blank=False, verbose_name='Скидка')
    photo_one = models.ImageField(upload_to='product_photos/')
    photo_two = models.ImageField(upload_to='product_photos/')
    photo_three = models.ImageField(upload_to='product_photos/')
