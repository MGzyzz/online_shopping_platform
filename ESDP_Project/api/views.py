import decimal

from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from accounts.models import Account
from shop.models import TimeDiscount, Product, Bucket, Order, OrderProducts
from shop.views import get_client_ip
from shop.views.bucket import BucketListView
from .serializers import TimeDiscountSerializer, BucketSerializer, ProductSerializer, OrderSerializer


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
            product = time_discount.product
            price = product.discounted_price if product.discounted_price else product.price

            if time_discount.discount:
                discounted_price = price - (
                        price * (time_discount.discount / 100))

            elif time_discount.discount_in_currency:
                discounted_price = price - time_discount.discount_in_currency

            else:
                discounted_price = 0

            time_discount.discounted_price = discounted_price
            time_discount.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except TimeDiscount.DoesNotExist:
            return Response({'error': 'Not found'})

    @action(detail=False, methods=['GET'], url_path='get-discount-by-product')
    def get_discount_by_product(self, request):
        product_id = request.query_params.get('product_id')

        try:
            discount = TimeDiscount.objects.get(product_id=product_id)

            return Response({'discount_id': discount.id})
        except TimeDiscount.DoesNotExist:
            return Response({'error': 'Discount not found for the product'})

    @action(detail=True, methods=['get'], url_path='check-start')
    def check_start(self, request, id=None):
        discount = self.get_object()

        start_date = discount.start_date.astimezone(timezone.get_current_timezone())
        now = timezone.now()

        if now >= start_date:
            return Response({'started': True})

        else:
            return Response({'started': False})


class BucketViewSet(viewsets.ModelViewSet):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer

    @action(detail=False, methods=['POST'])
    def add_to_cart(self, request, *args, **kwargs):
        shop_id = request.data.get('shop')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)
        user = request.data.get("user")

        ip_address = get_client_ip(request)

        try:
            user = Account.objects.get(user_id=user)
            created = Bucket.objects.create(user=user, product_id=product_id, shop_id=shop_id,
                                            quantity=quantity)

        except Account.DoesNotExist:
            created = Bucket.objects.create(ip_address=ip_address, product_id=product_id, shop_id=shop_id,
                                            quantity=quantity)

        self.get_discount(created)
        serializer = self.get_serializer(created)

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get_discount(item) -> None:
        product = item.product
        quantity = decimal.Decimal(item.quantity)
        item.unit_price = product.price * quantity

        if discount := product.discounted_price:
            item.unit_price = discount * quantity

        if TimeDiscount.objects.filter(product=product).exists():
            time_discount = TimeDiscount.objects.get(product=product)
            item.unit_price = time_discount.discounted_price * quantity
        item.save()

    @action(detail=True, methods=['DELETE'])
    def remove_from_cart(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @action(detail=True, methods=['PUT'])
    def update_quantity(self, request, *args, **kwargs):
        try:
            item_id = self.kwargs.get('pk')
            new_quantity = int(request.data.get('new_quantity'))
            item = Bucket.objects.get(id=item_id)
            item.unit_price = (item.unit_price/item.quantity) * new_quantity
            item.quantity = new_quantity
            item.save()

            bucket_all = Bucket.objects.filter(Q(ip_address=item.ip_address)) or Bucket.objects.filter(
                Q(user_id=item.user))

            total_price = sum(item.unit_price for item in bucket_all)
            product_id = item.product.id

            return JsonResponse({'success': True, "total_price": total_price, 'product_id': product_id,
                                 'unit_price': item.unit_price}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['POST'])
    def create_order(self, request, *args, **kwargs):
        data = request.data
        shop = data.get('shop')
        total = data.get('total')
        order = Order.objects.create(shop_id=shop, total=total)

        products = Bucket.objects.filter(id__in=data.get('products').split(','))
        self.add_products(products, order)

        order.payer_city = data.get('payer_city')
        order.payer_address = data.get('payer_address')
        order.payer_phone = data.get('payer_phone')
        order.payer_email = data.get('payer_email')
        order.payer_surname = data.get('payer_surname')
        order.payer_name = data.get('payer_name')
        order.payer_postal_code = data.get('payer_postal_code')
        order.save()

        if self.request.user.is_authenticated:
            order.payer = request.user
            return JsonResponse(data={'order_id': order.id, 'user_id': order.user.id}, status=status.HTTP_201_CREATED)

        return JsonResponse(data={'order_id': order.id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def add_products(products, order):
        for item in products:
            OrderProducts.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_per_product=item.unit_price,
            )
            item.delete()
