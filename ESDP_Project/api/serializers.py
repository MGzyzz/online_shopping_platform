from rest_framework import serializers
from shop.models import TimeDiscount


class TimeDiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeDiscount
        fields = '__all__'

    discounted_price = serializers.IntegerField(required=False)


