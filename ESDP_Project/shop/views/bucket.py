from django.utils import timezone
from django.views.generic import CreateView

from shop.forms import OrderForm
from shop.models import Bucket, Shop, Order, Product, TimeDiscount


class BucketListView(CreateView):
    template_name = 'orders/bucket.html'
    model = Order
    form_class = OrderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        shop_id = self.kwargs['shop_id']

        if user.is_authenticated:
            bucket_items = Bucket.objects.filter(user=user.id, shop_id=shop_id)
        else:
            ip_address = self.get_client_ip(self.request)
            bucket_items = Bucket.objects.filter(ip_address=ip_address, shop_id=shop_id)

        products = Product.objects.filter(id__in=bucket_items.values_list('product_id')).order_by('product_in_bucket')

        self.get_discount(bucket_items)

        context['total_price'] = sum(item.unit_price for item in bucket_items)
        context['shop'] = Shop.objects.get(id=self.kwargs['shop_id'])
        context['products'] = dict(zip(products, bucket_items))
        return context

    @staticmethod
    def get_discount(bucket_items) -> None:
        for item in bucket_items:
            product = item.product
            item.unit_price = product.price * item.quantity

            if discount := product.discounted_price:
                item.unit_price = discount * item.quantity

            if TimeDiscount.objects.filter(product=product).exists():
                time_discount = TimeDiscount.objects.get(product=product)
                item.unit_price = time_discount.discounted_price * item.quantity

    def get_client_ip(self, request) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
