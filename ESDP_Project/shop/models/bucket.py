from django.db import models

from accounts.models import User
from shop.models import Product


class Bucket(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_in_bucket'
    )
    quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name='Количество'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bucket_user'
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )
