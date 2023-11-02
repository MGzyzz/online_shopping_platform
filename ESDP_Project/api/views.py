from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from shop.models import TimeDiscount, Product, Bucket
from .serializers import TimeDiscountSerializer, BucketSerializer
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

            if time_discount.discount:
                discounted_price = time_discount.product.price - (
                        time_discount.product.price * (time_discount.discount / 100))

            elif time_discount.discount_in_currency:
                discounted_price = time_discount.product.price - time_discount.discount_in_currency

            else:
                discounted_price = 0

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


class BucketViewSet(viewsets.ModelViewSet):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer


    @action(detail=False, methods=['POST'])
    def add_to_cart(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)
        ip_address = self.get_client_ip(request)
        user = request.data.get("user")

        if user:
            user_id = request.data.get('user')
            # Попытка получить объект корзины пользователя
            created = Bucket.objects.filter(user_id=user_id, product_id=product_id).first()
            if created:
                # Обновление количества товара
                created.quantity += int(quantity)
                created.save()
            else:
                # Создание нового объекта корзины
                created = Bucket.objects.create(user_id=user_id, product_id=product_id, quantity=quantity)

        else:
            # Попытка получить объект корзины по IP-адресу
            created = Bucket.objects.filter(ip_address=ip_address, product_id=product_id).first()
            if created:
                # Обновление количества товара
                created.quantity += int(quantity)
                created.save()
            else:
                # Создание нового объекта корзины
                created = Bucket.objects.create(ip_address=ip_address, product_id=product_id, quantity=quantity)

        serializer = self.get_serializer(created)

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    @action(detail=True, methods=['DELETE'])
    def remove_from_cart(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


