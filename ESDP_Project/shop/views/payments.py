from django.views.generic import TemplateView

from shop.models import Order


class PaymentView(TemplateView):
    template_name = 'orders/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(id=self.kwargs['order_id'])
        context['order'] = order
        context['shop'] = order.shop
        return context