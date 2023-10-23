from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
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
        context['now'] = timezone.now()

        return context


class EditProduct(UpdateView):
    template_name = 'product/edit_product.html'
    context_object_name = 'product'
    model = Product
    form_class = ProductForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('shop_view', kwargs={'shop_id': self.kwargs['shop_id']})

    def form_valid(self, form):
        shop = get_object_or_404(Shop, id=self.kwargs['shop_id'])
        product = form.save(commit=False)
        product.shop_id = shop
        product.save()
        tags_string = form.cleaned_data['tags']
        product.tags.set(tags_string)

        uploaded_images_count = 0

        for i, image_obj in enumerate(product.images.all(), start=1):
            uploaded_image = self.request.FILES.get(f'photo_{i}')
            if uploaded_image:
                image_obj.image = uploaded_image
                image_obj.save()
                uploaded_images_count += 1

        return redirect(self.get_success_url())


class DeleteProduct(DeleteView):
    template_name = 'shop_templates/shop_view.html'
    context_object_name = 'product'
    model = Product
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('shop_view', kwargs={'shop_id': self.object.shop_id})


