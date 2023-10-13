from django.urls import path
from shop.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('shop/create', ShopCreateView.as_view(), name='shop_create')
]
