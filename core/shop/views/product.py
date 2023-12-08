from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from taggit.models import Tag

from shop.forms import ProductForm, ImagesForm, ProductKaspiForm
from shop.models import Images, Category, Product, Shop, City, PartnerShop
import httpx
from django.http import HttpResponse

class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create_product.html'
    extra_context = {
        'image_form': ImagesForm()
    }

    def has_permission(self):
        return Shop.objects.get(id=self.kwargs['shop_id']).user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.image_form = ImagesForm()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.image_form = ImagesForm(request.POST, request.FILES)

        if self.image_form.is_valid() and self.get_form().is_valid():
            return self.form_valid(self.get_form())

        return render(self.request, 'product/create_product.html',
                      {'form': self.get_form(), 'image_form': self.image_form})

    def form_valid(self, form):
        shop = get_object_or_404(Shop, id=self.kwargs['shop_id'])
        product = form.save(commit=False)
        product.shop = shop
        product.category = form.cleaned_data['category']

        if product.discount:

            if product.discount > 0:
                product.discounted_price = product.price - (product.price * (product.discount / 100))

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
            product.save()

    def form_invalid(self, form):
        return render(self.request, 'product/create_product.html', {'form': form})


class ProductListView(ListView):
    template_name = 'shop/products.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-created']

    def dispatch(self, request, *args, **kwargs):
        self.shop = get_object_or_404(Shop, id=self.kwargs['shop_id'])
        self.products = self.shop.products.all()
        return super().dispatch(request, *args, **kwargs)

    def get_allow_empty(self):
        allow_empty = True
        return allow_empty

    def get_queryset(self):
        if query := self.request.GET.get('search'):
            capitalized_query = query.capitalize()
            query = (Q(name__icontains=query) |
                     Q(description__icontains=query) |
                     Q(category__name__icontains=query) |
                     Q(tags__name__icontains=query) |
                     Q(name__icontains=capitalized_query) |
                     Q(description__icontains=capitalized_query) |
                     Q(category__name__icontains=capitalized_query) |
                     Q(tags__name__icontains=query))
            queryset = self.products.filter(query).distinct()
            return queryset
        if category_id := self.request.GET.get('category'):
            return self.shop.products.filter(category_id=category_id)
        return self.products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = self.shop
        context['now'] = timezone.now()
        context['categories'] = set([products.category for products in self.products])

        return context


class EditProduct(PermissionRequiredMixin, UpdateView):
    template_name = 'product/edit_product.html'
    context_object_name = 'product'
    model = Product
    form_class = ProductForm
    pk_url_kwarg = 'id'

    def has_permission(self):
        return Product.objects.get(id=self.kwargs['id']).shop.user == self.request.user

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

    def save_images(self):
        for image_id, image in self.request.FILES.items():
            old_image = get_object_or_404(Images, id=image_id)
            storage, path = old_image.image.storage, old_image.image.path
            storage.delete(path)
            old_image.image = image
            old_image.save()

    def form_valid(self, form):
        product = form.save(commit=False)
        product.category = form.cleaned_data['category']

        if product.discount:

            if product.discount > 0:
                product.discounted_price = product.price - (product.price * (product.discount / 100))

        self.new_category(product)
        product.save()

        tags_string = form.cleaned_data['tags']
        tags_string = [tag[:-1] if tag[-1] == ';' else tag for tag in tags_string]

        product.tags.set(tags_string)
        self.remove_all_tags_without_objects()

        self.save_images()

        return redirect(self.get_success_url())


class DeleteProduct(PermissionRequiredMixin, DeleteView):
    context_object_name = 'product'
    model = Product
    pk_url_kwarg = 'id'

    def has_permission(self):
        return self.product.shop.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, id=self.kwargs['id'])
        self.images = self.product.images.all()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        for image in self.images:
            storage, path = image.image.storage, image.image.path
            storage.delete(path)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('shop_products', kwargs={'id': self.object.shop_id})


class DetailProduct(DetailView):
    template_name = 'product/detail_product.html'
    context_object_name = 'product'
    model = Product
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        self.product = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['shop'] = self.product.shop
        context['attributes'] = self.product.attributes.all()
        parameters = {}
        for attribute in context['attributes']:
            if ',' in attribute.value:
                parameters[attribute.name] = attribute.value.split(',')
        context['parameters'] = parameters
        return context


class ShopProductView(PermissionRequiredMixin, ListView):
    template_name = 'profile/profile_product_list.html'
    context_object_name = 'products'
    model = Product
    pk_url_kwarg = 'id'
    paginate_by = 20

    def has_permission(self):
        return self.shop.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.shop = get_object_or_404(Shop, id=self.kwargs['id'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.shop.products.all()
        if query := self.request.GET.get('search'):
            capitalized_query = query.capitalize()
            query = (Q(name__icontains=query) |
                     Q(description__icontains=query) |
                     Q(category__name__icontains=query) |
                     Q(tags__name__icontains=query) |
                     Q(name__icontains=capitalized_query) |
                     Q(description__icontains=capitalized_query) |
                     Q(category__name__icontains=capitalized_query) |
                     Q(tags__name__icontains=query))
            queryset = queryset.filter(query).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = self.shop
        return context


class ProductKaspiView(View):
    template_name = 'product/product_kaspi.html'
    KASPI_XML_URL = 'http://kaspixml:5050/generate_xml'
    CITY_CHOICES = [(471010000, 'Актау'), (151010000, 'Актобе'), (750000000, 'Алматы'), (511610000, 'Арысь'),
                    (710000000, 'Астана'), (231010000, 'Атырау'), (351810000, 'Жезказган'),
                    (351010000, 'Караганда'),
                    (195220100, 'Каскелен'), (191610000, 'Капшагай'), (111010000, 'Кокшетау'),
                    (314851205, 'Кордай'),
                    (391010000, 'Костанай'), (233620100, 'Кульсары'), (431010000, 'Кызылорда'),
                    (551010000, 'Павлодар'),
                    (591010000, 'Петропавловск'), (392410000, 'Рудный'), (352310000, 'Сатпаев'),
                    (632810000, 'Семей'),
                    (196220100, 'Талгар'), (191010000, 'Талдыкорган'), (311010000, 'Тараз'),
                    (352410000, 'Темиртау'),
                    (271010000, 'Уральск'), (631010000, 'Усть-Каменогорск'), (511010000, 'Шымкент'),
                    (552210000, 'Экибастуз'),
                    (194020100, 'Есик'), (512610000, 'Туркестан'), (117020100, 'Щучинск'), (471810000, 'Жанаозен'),
                    (515420100, 'Сарыагаш'), (352810000, 'Шахтинск'), (117055900, 'Шиели'), (273620100, 'Аксай'),
                    (514420100, 'Жетысай'), (351610000, 'Балхаш'), (551610000, 'Аксу'), (433220100, 'Аральск'),
                    (431910000, 'Байконыр'), (473630100, 'Бейнеу'), (195620100, 'Жаркент'), (634620100, 'Зайсан'),
                    (316220100, 'Каратау'), (612010000, 'Кентау'), (314851205, 'Кордай'), (392010000, 'Лисаковск'),
                    (352210000, 'Сарань'), (111810000, 'Степногорск'), (192610000, 'Текели'),
                    (616420100, 'Шардара'),
                    (316621100, 'Шу'), (156420100, 'Риддер'), (634820100, 'Алтай'), (271035100, 'Зачаганск'),
                    (153220100, 'Алга'), (156020100, 'Хромтау'), (391610000, 'Аркалык'), (395430100, 'Тобыл'),
                    (554230100, 'Железинка'), (394420100, 'Житикара'), (116651100, 'Косшы'), (633420100, 'Аягоз'),
                    (634030100, 'Глубокое'), (632210000, 'Курчатов'), (636820100, 'Шемонаиха'), (353220100, 'Абай'),
                    (474630100, 'Шетпе'), (475220100, 'Форт-Шевченко'), (474239100, 'Жетыбай'),
                    (474230100, 'Курык'),
                    (113220100, 'Акколь'), (515820100, 'Ленгер'), (195020100, 'Уштобе'), (154820100, 'Кандыагаш'),
                    (194230100, 'Узынагаш'), (515230100, 'Аксукент')
                    ]

    def get(self, request, shop_id):
        for code, name in self.CITY_CHOICES:
            City.objects.get_or_create(city_code=code, name=name)

        shop = Shop.objects.get(id=shop_id)

        try:
            partner_shop = PartnerShop.objects.get(shop_id=shop_id)
            partner_id = partner_shop.partner_id

        except PartnerShop.DoesNotExist:
            partner_id = None

        form = ProductKaspiForm(shop_id=shop_id, initial_partner_id=partner_id)

        return render(request, self.template_name, {'form': form, 'shop': shop})

    def post(self, request, shop_id):
        form = ProductKaspiForm(request.POST, shop_id=shop_id)

        if form.is_valid():
            form.save()

            data = {
                'offers': [],
                'partner_id': form.cleaned_data['partner_id']
            }

            for product in form.cleaned_data['products']:
                some_product = {
                    'id': product.id,
                    'shop_id': product.shop.id,
                    'price': int(product.price),
                    'quantity': product.quantity,
                    'name': product.name,
                    'city_code': form.cleaned_data['city'].city_code
                    }

                data['offers'].append(some_product)

            try:
                headers = {"Content-Type": "application/json"}
                response = httpx.post(self.KASPI_XML_URL, json=data, headers=headers)

                if response.status_code == 200:
                    return HttpResponse(response, content_type='application/xml')

                else:
                    return HttpResponse(f'Error')

            except Exception as e:
                return HttpResponse(f'{e}')

        return render(request, self.template_name, {'form': form})
