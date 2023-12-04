from django.db import models


class PartnerShop(models.Model):
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, related_name='partner')
    partner_id = models.CharField(max_length=150, verbose_name='ID партнера')
