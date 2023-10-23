from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from shop.forms import ShopModelForm
from shop.models import Shop
from django.urls import reverse_lazy


class Home(TemplateView):
    template_name = 'base.html'


class ShopCreateView(CreateView):
    model = Shop
    template_name = 'shop_create_update.html'
    form_class = ShopModelForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class ShopUpdateView(UpdateView):
    model = Shop
    template_name = 'shop_update.html'
    form_class = ShopModelForm
    context_object_name = 'shop'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('home')


class ShopListView(ListView):
    template_name = 'shop_list_view.html'
    model = Shop
    context_object_name = 'shops'
    paginate_by = 5
