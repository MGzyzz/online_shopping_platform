from django.urls import path
from .views import *
from .views.product import DetailProduct

urlpatterns = [
    path('create', ShopCreateView.as_view(), name='shop_create'),
    path('update/<int:id>', ShopUpdateView.as_view(), name='shop_update'),
    path('<int:shop_id>/create_product/', ProductCreateView.as_view(), name='create_product'),
    path('', ShopListView.as_view(), name='home'),
    path('client/<int:shop_id>', ProductListView.as_view(), name='shop_view'),
    path('product/<int:id>/edit/', EditProduct.as_view(), name='edit_product'),
    path('product/<int:id>/delete/', DeleteProduct.as_view(), name='delete_product'),
    path('product/<int:id>/attributes/add/', AttributesCreateView.as_view(), name='add_attributes'),
    path('product/<int:id>/attributes/update/', AttributesUpdateView.as_view(), name='update_attributes'),
    path('product/<int:id>', DetailProduct.as_view(), name='detail_product')
]
