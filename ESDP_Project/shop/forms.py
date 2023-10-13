from django import forms
from .models import ShopModel


class ShopModelForm(forms.ModelForm):
    class Meta:
        model = ShopModel
        fields = ['name', 'logo', 'description', 'theme']
