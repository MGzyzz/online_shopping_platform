from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from taggit.models import Tag

from shop.forms import ProductForm, ImagesForm
from shop.models import Images, Category, Product, Shop


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

        return render(self.request, 'product/create_product.html',
                      {'form': self.get_form(), 'image_form': self.image_form})

    def form_valid(self, form):
        shop = get_object_or_404(Shop, id=self.kwargs['shop_id'])

        product = form.save(commit=False)
        product.shop = shop
        product.category = form.cleaned_data['category']

        self.new_category(product)

        product.save()

        tags_string = form.cleaned_data['tags']
        product.tags.set(tags_string)

        images = self.image_form.cleaned_data['image']

        for image in images:
            Images.objects.create(product=product, image=image)

        return redirect('add_attributes', id=product.id)

    def new_category(self, product):
        if new_category := self.request.POST['new_category']:
            new_category = new_category.capitalize()

            if not Category.objects.filter(name=new_category).exists():
                Category.objects.create(name=new_category)

            product.category = Category.objects.get(name=new_category)

    def form_invalid(self, form):
        return render(self.request, 'product/create_product.html', {'form': form})


class ProductListView(ListView):
    template_name = 'shop/shop_view.html'
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
        context['now'] = timezone.now()

        return context


class EditProduct(UpdateView):
    template_name = 'product/edit_product.html'
    context_object_name = 'product'
    model = Product
    form_class = ProductForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('update_attributes', kwargs={'id': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        self.image_form = ImagesForm()
        self.images = self.get_object().images.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tags = self.object.tags
        data = {
            'name': self.object.name,
            'description': self.object.description,
            'vendor_code': self.object.vendor_code,
            'quantity': self.object.quantity,
            'price': self.object.price,
            'discount': self.object.discount,
            'tags': '; '.join(tag.name for tag in tags.all()) if tags.exists() else '',
            'category': self.object.category,
        }

        context['form'] = ProductForm(initial=data)
        context['images'] = self.images

        return context

    def new_category(self, product):
        if new_category := self.request.POST['new_category']:
            new_category = new_category.capitalize()

            if not Category.objects.filter(name=new_category).exists():
                Category.objects.create(name=new_category)

            product.category = Category.objects.get(name=new_category)

    def remove_all_tags_without_objects(self):
        for tag in Tag.objects.all():
            if tag.taggit_taggeditem_items.count() == 0:
                tag.delete()

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()

        tags_string = form.cleaned_data['tags']
        tags_string = [tag[:-1] if tag[-1] == ';' else tag for tag in tags_string]
        product.tags.set(tags_string)
        self.remove_all_tags_without_objects()

        self.new_category(product)

        for image_id, image in self.request.FILES.items():
            old_image = get_object_or_404(Images, id=image_id)
            old_image.image = image
            old_image.save()

        return redirect(self.get_success_url())


class DeleteProduct(DeleteView):
    template_name = 'shop/shop_view.html'
    context_object_name = 'product'
    model = Product
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('shop_view', kwargs={'shop_id': self.object.shop_id})


class DetailProduct(DetailView):
    template_name = 'product/detail_product.html'
    context_object_name = 'product'
    model = Product
    pk_url_kwarg = 'id'

