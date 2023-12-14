from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from .models import Shop, Product, Images, Category, PartnerProduct, City, PartnerShop


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


class ProductKaspiForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': ''}),
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.RadioSelect,
    )

    class Meta:
        model = PartnerShop
        fields = ['partner_id']
        widgets = {
            'partner_id': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        shop_id = kwargs.pop('shop_id', None)
        self.shop_id = shop_id

        initial_partner_id = kwargs.pop('initial_partner_id', None)

        super().__init__(*args, **kwargs)

        if initial_partner_id:
            self.initial['partner_id'] = initial_partner_id

        if shop_id:
            self.fields['products'].queryset = Product.objects.filter(shop_id=shop_id)

    def save(self, commit=True):
        partner_shop = PartnerShop.objects.get_or_create(
            shop_id=self.shop_id,
            partner_id=self.cleaned_data['partner_id']
        )

        for product in self.cleaned_data['products']:
            PartnerProduct.objects.get_or_create(
                product=product,
                partner_shop=partner_shop[0],
                city=self.cleaned_data['city']
            )

        return PartnerShop
