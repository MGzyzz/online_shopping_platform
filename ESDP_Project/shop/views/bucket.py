from django.db.models import When, Case
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from shop.forms import OrderForm
from shop.models import Bucket, Shop, Order, Product, TimeDiscount, OrderProducts


class BucketListView(CreateView):
    template_name = 'orders/bucket.html'
    model = Order
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        self.shop_id = self.kwargs['shop_id']

        if self.user.is_authenticated:
            self.bucket_items = Bucket.objects.filter(user=self.user.id, shop_id=self.shop_id)
        else:
            ip_address = self.get_client_ip(self.request)
            self.bucket_items = Bucket.objects.filter(ip_address=ip_address, shop_id=self.shop_id)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        bucket_ids = self.bucket_items.values_list('product_id', flat=True)
        order_conditions = [When(id=id_val, then=pos) for pos, id_val in enumerate(bucket_ids, start=1)]
        products = Product.objects.filter(id__in=bucket_ids).order_by(Case(*order_conditions))

        self.get_discount(self.bucket_items)
        self.check_quantity(self.bucket_items)

        context['total_price'] = sum(item.unit_price for item in self.bucket_items)
        context['shop'] = Shop.objects.get(id=self.shop_id)
        context['products'] = dict(zip(products, self.bucket_items))
        context['items'] = ', '.join(str(item.id) for item in self.bucket_items)

        return context

    def check_quantity(self, bucket_items):
        for item in bucket_items:
            if item.product.quantity == 0:
                item.delete()

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

            item.save()

    @staticmethod
    def get_client_ip(request) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    def get_success_url(self):
        return reverse_lazy('payment', kwargs={'order_id': self.object.id})
