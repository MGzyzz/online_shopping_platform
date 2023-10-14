from django import forms
from .models import ShopModel, ProductModel


class ShopModelForm(forms.ModelForm):
    class Meta:
        model = ShopModel
        fields = ['name', 'logo', 'description', 'theme']


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['name', 'description', 'vendor_code', 'quantity', 'price', 'discount', 'photo_one', 'photo_two', 'photo_three']