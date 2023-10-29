from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, ListView

from accounts.forms import LoginForm
from shop.forms import ShopModelForm
from shop.models import Shop
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


class ShopUpdateView(PermissionRequiredMixin, UpdateView):
    model = Shop
    template_name = 'shop/shop_update.html'
    form_class = ShopModelForm
    context_object_name = 'shop'
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        self.shop = get_object_or_404(Shop, id=self.kwargs['id'])
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        return self.shop.user == self.request.user

    def form_valid(self, form):
        shop = form.save(commit=False)
        old_logo = self.shop.logo
        storage, path = old_logo.storage, old_logo.path
        storage.delete(path)
        shop.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class ShopListView(ListView):
    template_name = 'main.html'
    model = Shop
    context_object_name = 'shops'
    paginate_by = 5
    extra_context = {
        'form': LoginForm()
    }
