from django.views.generic import TemplateView, CreateView, UpdateView, ListView

from accounts.forms import LoginForm
from shop.forms import ShopModelForm
from shop.models import Shop, Product
from django.urls import reverse_lazy


class ShopCreateView(CreateView):
    model = Shop
    template_name = 'shop/shop_create_update.html'
    form_class = ShopModelForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class ShopUpdateView(UpdateView):
    model = Shop
    template_name = 'shop/shop_update.html'
    form_class = ShopModelForm
    context_object_name = 'shop'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('home')


class ShopListView(ListView):
    template_name = 'main.html'
    model = Shop
    context_object_name = 'shops'
    paginate_by = 5
    extra_context = {
        'form': LoginForm(),
        "products": Product.objects.all()
    }
