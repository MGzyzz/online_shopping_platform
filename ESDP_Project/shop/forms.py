from django import forms
from .models import Shop, Product


class ShopModelForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'logo', 'description', 'theme']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'vendor_code', 'quantity', 'price', 'discount', 'photo_one', 'photo_two', 'photo_three']