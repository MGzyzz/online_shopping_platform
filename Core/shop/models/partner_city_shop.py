from django.db import models


class PartnerCityShop(models.Model):
    partner_product = models.ForeignKey('shop.PartnerProduct', on_delete=models.CASCADE, related_name='partner_city')
    city = models.ForeignKey('shop.City', on_delete=models.CASCADE, related_name='partner_city')
