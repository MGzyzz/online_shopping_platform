from django import forms
from .models import Shop, Product, Images


class ShopModelForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'logo', 'description', 'theme']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'vendor_code', 'quantity', 'price', 'discount']


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']
