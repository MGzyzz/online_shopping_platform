from django.views.generic import TemplateView, CreateView, UpdateView
from .forms import ShopModelForm, ProductForm
from shop.models import ShopModel, ProductModel
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect


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


class ProductCreateView(CreateView):
    model = ProductModel
    form_class = ProductForm
    template_name = 'create_product.html'

    def form_valid(self, form):
        shop = get_object_or_404(ShopModel, id=self.kwargs['shop_id'])
        product = form.save(commit=False)
        product.shop_id = shop
        product.save()
        form.save()
        return redirect('home')

    def form_invalid(self, form):
        return render(self.request, 'create_product.html', {'form': form})
