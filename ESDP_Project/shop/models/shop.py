from django.db import models
from django.db.models import TextChoices

from core import settings


class Themes(TextChoices):
    DARK = 'Dark', 'Темная'
    LIGHT = 'Light', 'Светлая'
    RED = 'Red', 'Красная'


class Shop(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='shop_user'
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Название магазина',
        unique=True
    )
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=settings.LOGO_IMG_UPLOAD_PATH,
        verbose_name='Логотип магазина',
        default='default_img/default'
    )
    description = models.TextField(
        null=True,
        blank=True,
        max_length=2500,
        verbose_name='Описание магазина'
    )
    theme = models.CharField(
        max_length=255,
        choices=Themes.choices,
        default=Themes.DARK,
        verbose_name='Тема магазина'
    )

