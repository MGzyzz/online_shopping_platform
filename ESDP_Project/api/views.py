from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from shop.models import TimeDiscount
from .serializers import TimeDiscountSerializer
from datetime import datetime


class TimeDiscountViewSet(viewsets.ModelViewSet):
    queryset = TimeDiscount.objects.all()
    serializer_class = TimeDiscountSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = TimeDiscountSerializer(data=request.data)

        if serializer.is_valid():
            time_discount = serializer.save()

            discounted_price = time_discount.product.price - (
                        time_discount.product.price * (time_discount.discount / 100))
            time_discount.discounted_price = discounted_price

            time_discount.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['get'], url_path='check-expiration')
    def check_expiration(self, request, id=None):
        discount = self.get_object()

        end_date = discount.end_date.astimezone(timezone.get_current_timezone())
        now = timezone.now()

        if now >= end_date:
            discount.delete()

            return Response({'expired': True})
        else:

            return Response({'expired': False})
