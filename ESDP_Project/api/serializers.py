from rest_framework import serializers
from shop.models import TimeDiscount
from django.utils import timezone


class TimeDiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeDiscount
        fields = '__all__'

    start_date = serializers.DateTimeField(
        required=True,
        error_messages={
            'required': 'Поле "Начало скидки" обязательно для заполнения.',
            'invalid': 'Введите корректные данные в поле "Начало скидки"'
        }
    )

    end_date = serializers.DateTimeField(
        required=True,
        error_messages={
            'required': 'Поле "Конец скидки" обязательно для заполнения.',
            'invalid': 'Введите корректные данные в поле "Конец скидки"'
        }
    )

    discount = serializers.IntegerField(
        required=False,
        error_messages={
            'invalid': 'Введите корректные данные в поле "Скидка в процентах"'
        }
    )

    discount_in_currency = serializers.IntegerField(
        required=False,
        error_messages={
            'invalid': 'Введите корректные данные в поле "Скидка в денежном эквиваленте"'
        }
    )

    discounted_price = serializers.IntegerField(required=False)

    def validate_start_date(self, value):
        current_datetime = timezone.now()
        current_datetime_without = current_datetime.replace(microsecond=0, second=0)

        if current_datetime_without > value:
            raise serializers.ValidationError("Дата и время начала скидки должна быть в будущем или настоящем ")

        return value

    def validate_end_date(self, value):
        current_datetime = timezone.now()

        if value <= current_datetime:
            raise serializers.ValidationError("Дата и время окончания скидки должна быть в будущем.")

        return value

    def validate_discount(self, value):
        if value < 1 or value > 99:
            raise serializers.ValidationError("Скидка должна быть в диапазоне от 1 до 99.")

        return value

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        discount = data.get('discount')
        discount_in_currency = data.get('discount_in_currency')

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("Дата и время начала должна быть меньше даты и времени окончания.")

        if not discount and not discount_in_currency:
            raise serializers.ValidationError(
                "Должно быть заполнено хотя бы одно из полей: 'discount' или 'discount_in_currency'.")

        if discount and discount_in_currency:
            raise serializers.ValidationError(
                "Заполнено оба поля: 'discount' и 'discount_in_currency', оставьте только одно поле заполненным.")

        return data


