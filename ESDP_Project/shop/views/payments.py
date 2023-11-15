from django.views.generic import TemplateView

from shop.models import Order


class PaymentView(TemplateView):
    template_name = 'orders/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(id=self.kwargs['order_id'])
        return context