from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView
from .forms import ShopModelForm, ProductForm, ImagesForm
from shop.models import Shop, Product
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Images, Category
from accounts.models import User


# Create your views here.

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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create_product.html'
    extra_context = {
        'image_form': ImagesForm()
    }

    def dispatch(self, request, *args, **kwargs):
        self.image_form = ImagesForm()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.image_form = ImagesForm(request.POST, request.FILES)
        if self.image_form.is_valid():
            return self.form_valid(self.get_form())
        else:
            return render(self.request, 'product/create_product.html',
                          {'form': self.get_form(), 'image_form': self.image_form})

    def form_valid(self, form):
        shop = get_object_or_404(Shop, id=self.kwargs['shop_id'])

        product = form.save(commit=False)
        product.shop = shop
        product.category = form.cleaned_data['category']

        self.new_category(product)
        product.save()

        images = self.image_form.cleaned_data['image']

        for image in images:
            Images.objects.create(product=product, image=image)

        return redirect('home')

    def new_category(self, product):
        if new_category := self.request.POST['new_category']:
            new_category = new_category.capitalize()

            if not Category.objects.filter(name=new_category).exists():
                Category.objects.create(name=new_category)

            product.category = Category.objects.get(name=new_category)

    def form_invalid(self, form):
        return render(self.request, 'product/create_product.html', {'form': form})


class ProductListView(ListView):
    template_name = 'shop_templates/shop_view.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5

    def get_allow_empty(self):
        allow_empty = True
        return allow_empty

    def get_queryset(self):
        shop = get_object_or_404(Shop, id=self.kwargs['shop_id'])
        return Product.objects.filter(shop_id=shop)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop, id=self.kwargs['shop_id'])
        context['shop'] = shop

        return context


class EditProduct(UpdateView):
    template_name = 'product/edit_product.html'
    context_object_name = 'product'
    model = Product
    form_class = ProductForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('shop_view', kwargs={'shop_id': self.object.shop_id_id})

    def form_valid(self, form):
        shop = get_object_or_404(Shop, id=self.kwargs['shop_id'])
        product = form.save(commit=False)

        product.shop_id = shop
        product.save()

        uploaded_images_count = 0

        for i, image_obj in enumerate(product.images.all(), start=1):
            uploaded_image = self.request.FILES.get(f'photo_{i}')
            if uploaded_image:
                image_obj.image = uploaded_image
                image_obj.save()
                uploaded_images_count += 1

        return redirect(self.get_success_url())


class DeleteProduct(DeleteView):
    template_name = 'shop/shop_view.html'
    context_object_name = 'product'
    model = Product
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('shop_view', kwargs={'shop_id': self.object.shop_id_id})
