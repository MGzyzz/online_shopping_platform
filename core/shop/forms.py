from django import forms
from django.core.validators import FileExtensionValidator

from .models import Shop, Product, Images, Category, PartnerProduct, City, PartnerShop, Order


class ShopModelForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'logo', 'description', 'theme', 'partner_id']


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'vendor_code', 'quantity', 'price', 'discount', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px'}),
            'vendor_code': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)

        return result


class ImagesForm(forms.ModelForm):
    image = MultipleImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])

    class Meta:
        model = Images
        fields = ['image']

    def clean(self):
        images = self.cleaned_data.get("image")

        if images and not len(images) <= 3:
            raise forms.ValidationError({'image': "Максимум 3 изображения"})

        return self.cleaned_data


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payer_name', 'payer_surname', 'payer_phone', 'payer_email', 'payer_city', 'payer_address',
                  'payer_postal_code']
        widgets = {
            'payer_name': forms.TextInput(attrs={'class': 'form-control', 'required': True, }),
            'payer_surname': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'payer_phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'payer_email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'payer_city': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'payer_address': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'payer_postal_code': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        label='Search:',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Введите название магазина'})
    )
