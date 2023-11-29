from django.db.models import When, Case
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from shop.forms import OrderForm
from shop.models import Bucket, Shop, Order, Product
from .additional_functions import get_client_ip, get_discount


class BucketListView(CreateView):
    template_name = 'orders/bucket.html'
    model = Order
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        self.shop_id = self.kwargs['shop_id']

        try:
            self.bucket_items = Bucket.objects.filter(user=self.user.account, shop_id=self.shop_id,
                                                      product__quantity__gt=0)
        except Bucket.DoesNotExist:
            ip_address = get_client_ip(self.request)
            self.bucket_items = Bucket.objects.filter(ip_address=ip_address, shop_id=self.shop_id,
                                                      product__quantity__gt=0)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        bucket_ids = self.bucket_items.values_list('product_id', flat=True)
        order_conditions = [When(id=id_val, then=pos) for pos, id_val in enumerate(bucket_ids, start=1)]
        products = Product.objects.filter(id__in=bucket_ids).order_by(Case(*order_conditions))

        self.get_form_data(context)
        for item in self.bucket_items:
            get_discount(item)

        context['bucket'] = self.bucket_items
        context['total_price'] = sum(item.unit_price for item in self.bucket_items)
        context['shop'] = Shop.objects.get(id=self.shop_id)
        context['products'] = dict(zip(products, self.bucket_items))
        context['items'] = ', '.join(str(item.id) for item in self.bucket_items)

        return context

    def get_form_data(self, context):
        try:
            account = self.user.account
            data = {
                'payer_name': self.user.first_name,
                'payer_surname': self.user.last_name,
                'payer_email': self.user.email,
                'payer_phone': self.user.phone,
                'payer_city': account.city,
                'payer_address': account.address,
                'payer_postal_code': account.postal_code,
            }
            context['form'] = OrderForm(initial=data)
        except AttributeError:
            pass

    def get_success_url(self):
        return reverse_lazy('payment', kwargs={'order_id': self.object.id})


class OrderListView(ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = Shop.objects.get(id=self.kwargs['shop_id'])
        return context

    def get_queryset(self):
        try:
            return Order.objects.filter(shop__id=self.kwargs['shop_id'], account=self.request.user.account)
        except AttributeError:
            return Order.objects.filter(shop__id=self.kwargs['shop_id'], user_ip=get_client_ip(self.request))