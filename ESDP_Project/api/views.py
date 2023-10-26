from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from shop.models import TimeDiscount
from .serializers import TimeDiscountSerializer
from datetime import datetime


class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return JsonResponse({
            'status': 200
        })


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

    @action(detail=False, methods=['GET'], url_path='get-discount-by-product')
    def get_discount_by_product(self, request):
        product_id = request.query_params.get('product_id')

        try:
            discount = TimeDiscount.objects.get(product_id=product_id)

            return Response({'discount_id': discount.id})
        except TimeDiscount.DoesNotExist:
            return Response({'error': 'Discount not found for the product'}, status=404)
