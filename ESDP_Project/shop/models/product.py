from django.db import models
from django.db.models import TextChoices
from shop.models import Shop
from taggit.managers import TaggableManager


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Название продукта')
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание')
    vendor_code = models.IntegerField(unique=True, null=False, blank=False, verbose_name='Код Поставщика')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.PositiveIntegerField(default=0, null=False, blank=False, verbose_name='Цена')
    discount = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='Скидка')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='products',
                                 verbose_name='Категория', null=True)
    tags = TaggableManager(blank=True, verbose_name='Тэги')