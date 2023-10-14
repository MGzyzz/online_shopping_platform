from django.urls import path
from shop.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('shop/create', ShopCreateView.as_view(), name='shop_create'),
    path('shop/update/<int:id>', ShopUpdateView.as_view(), name='shop_update'),
    path('shop/<int:shop_id>/create_product/', ProductCreateView.as_view(), name='create_product')
]
