from django.db import models


class TimeDiscount(models.Model):
    product = models.OneToOneField('shop.Product', on_delete=models.CASCADE, related_name='time_discount')
    discount = models.PositiveIntegerField(null=True, blank=True)
    discount_in_currency = models.PositiveIntegerField(null=True, blank=True)
    discounted_price = models.PositiveIntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
