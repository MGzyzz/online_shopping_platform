from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from shop.models import Attributes, Product


class AttributesCreateView(CreateView):
    model = Attributes
    template_name = 'product/add_attributes.html'
    fields = ['name', 'value']

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['id'])
        data = dict(zip(request.POST.getlist('name'), request.POST.getlist('value')))
        for name, value in data.items():
            Attributes.objects.create(product=product, name=name, value=value)
        return render(request, 'product/add_attributes.html')