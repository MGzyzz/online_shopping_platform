import random

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView

from accounts.forms import LoginForm
from shop.forms import ShopModelForm
from shop.models import Shop, Product, Bucket
from django.urls import reverse_lazy

from shop.models.bucket import Bucket


class ShopCreateView(LoginRequiredMixin, CreateView):
    model = Shop
    template_name = 'shop/shop_create_update.html'
    form_class = ShopModelForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'id': self.request.user.id})


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
        return reverse_lazy('profile', kwargs={'id': self.request.user.id})


class ShopListView(ListView):
    template_name = 'main.html'
    model = Shop
    context_object_name = 'shops'
    paginate_by = 5
    extra_context = {
        'form': LoginForm(),
    }



class ShopDeleteView(PermissionRequiredMixin, DeleteView):
    model = Shop
    pk_url_kwarg = 'id'

    def has_permission(self):
        return self.shop.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.shop = get_object_or_404(Shop, id=self.kwargs['id'])
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        old_logo = self.shop.logo
        storage, path = old_logo.storage, old_logo.path
        storage.delete(path)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'id': self.request.user.id})


class ShopMainView(ListView):
    template_name = 'shop/shop_main.html'
    model = Product
    context_object_name = 'products'

    def dispatch(self, request, *args, **kwargs):
        self.shop = get_object_or_404(Shop, id=self.kwargs['shop_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.shop.products.filter(quantity__gt=0)
        categories = set([products.category for products in products])
        category_product = {}
        context['shop'] = self.shop
        context['products'] = products[:3]
        context['now'] = timezone.now()

        for category in categories:
            category_product[category] = products.filter(category=category)[:3]
        context['category_product'] = category_product

        return context