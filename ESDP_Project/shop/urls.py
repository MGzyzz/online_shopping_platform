from django.urls import path
from .views import *

urlpatterns = [
    path('create', ShopCreateView.as_view(), name='shop_create'),
    path('update/<int:id>', ShopUpdateView.as_view(), name='shop_update'),
    path('<int:shop_id>/create_product/', ProductCreateView.as_view(), name='create_product'),
    path('list/<int:user_id>/', ShopListView.as_view(), name='shop_list'),
    path('client/<int:shop_id>', ProductListView.as_view(), name='shop_view'),
    path('client/<int:shop_id>/edit/<int:id>/', EditProduct.as_view(), name='edit_product'),
    path('client/<int:shop_id>/delete/<int:id>/', DeleteProduct.as_view(), name='delete_product'),
    path('<int:id>/attributes/add/', AttributesCreateView.as_view(), name='add_attributes'),
]
