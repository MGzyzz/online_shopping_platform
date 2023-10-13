from django.views.generic import TemplateView, CreateView, UpdateView
from .forms import ShopModelForm
from shop.models import ShopModel
from django.urls import reverse_lazy


# Create your views here.

class Home(TemplateView):
    template_name = 'base.html'


class ShopCreateView(CreateView):
    model = ShopModel
    template_name = 'shop_create_update.html'
    form_class = ShopModelForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class ShopUpdateView(UpdateView):
    model = ShopModel
    template_name = 'shop_update.html'
    form_class = ShopModelForm
    context_object_name = 'shop'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('home')
