from django.db.models import When, Case
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from accounts.models import User
from shop.forms import OrderForm
from shop.models import Bucket, Shop, Order, Product, TimeDiscount, OrderProducts
from .get_ip import get_client_ip


class BucketListView(CreateView):
    template_name = 'orders/bucket.html'
    model = Order
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        self.shop_id = self.kwargs['shop_id']

        try:
            self.bucket_items = Bucket.objects.filter(user=self.user.account, shop_id=self.shop_id)
        except:
            ip_address = get_client_ip(self.request)
            self.bucket_items = Bucket.objects.filter(ip_address=ip_address, shop_id=self.shop_id)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        bucket_ids = self.bucket_items.values_list('product_id', flat=True)
        order_conditions = [When(id=id_val, then=pos) for pos, id_val in enumerate(bucket_ids, start=1)]
        products = Product.objects.filter(id__in=bucket_ids).order_by(Case(*order_conditions))

        self.check_quantity(self.bucket_items)
        self.get_form_data(context)

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




    def check_quantity(self, bucket_items):
        for item in bucket_items:
            if item.product.quantity == 0:
                item.delete()



    def get_success_url(self):
        return reverse_lazy('payment', kwargs={'order_id': self.object.id})
