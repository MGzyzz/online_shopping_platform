from rest_framework import serializers
from shop.models import TimeDiscount
from django.utils import timezone


class TimeDiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeDiscount
        fields = '__all__'

    discounted_price = serializers.IntegerField(required=False)

    def validate_start_date(self, value):
        current_datetime = timezone.now()

        if value < current_datetime:
            raise serializers.ValidationError("Дата начала скидки должна быть в будущем или настоящем ")

        return value

    def validate_end_date(self, value):
        current_datetime = timezone.now()

        if value <= current_datetime:
            raise serializers.ValidationError("Дата окончания скидки должна быть в будущем.")

        return value

    def validate_discount(self, value):
        if value < 1 or value > 99:
            raise serializers.ValidationError("Скидка должна быть в диапазоне от 1 до 99.")

        return value


