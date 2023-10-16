from django.views.generic import TemplateView, CreateView, UpdateView, ListView
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


class ShopViewList(ListView):
    template_name = 'shop_view_list.html'
    model = ShopModel
    context_object_name = 'shops'
    paginate_by = 5


class ShopView(ListView):
    template_name = 'shop/shop_view.html'
    model = ProductModel
    context_object_name = 'products'
    paginate_by = 5


    def get_allow_empty(self):
        allow_empty = True
        return allow_empty

    def get_queryset(self):
        shop = get_object_or_404(ShopModel, id=self.kwargs['shop_id'])
        return ProductModel.objects.filter(shop_id=shop)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(ShopModel, id=self.kwargs['shop_id'])
        context['shop'] = shop
        return context