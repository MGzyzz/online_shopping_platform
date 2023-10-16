from django.db import models


class TimeDiscount(models.Model):
    product = models.ForeignKey('shop.ProductModel', on_delete=models.CASCADE, related_name='time_discount')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
