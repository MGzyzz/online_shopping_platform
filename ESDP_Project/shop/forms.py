from django import forms
from .models import Shop, Product, Images, Category


class ShopModelForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'logo', 'description', 'theme']


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'vendor_code', 'quantity', 'price', 'discount', 'tags']


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']
