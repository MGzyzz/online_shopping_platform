from django.db import models


class TimeDiscount(models.Model):
    product = models.ForeignKey('shop.ProductModel', on_delete=models.CASCADE, related_name='time_discount')
    discount = models.PositiveIntegerField(default=0)
    discounted_price = models.PositiveIntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
