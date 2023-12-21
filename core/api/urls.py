from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeDiscountViewSet, LogoutView, BucketViewSet, ProductViewSet, user_detail_api_view, \
   product_list_xml, TelegramShopsViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register('time_discount', TimeDiscountViewSet)
router.register('bucket', BucketViewSet)
router.register('product', ProductViewSet)
router.register('shop_for_telegram', TelegramShopsViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('login/', obtain_auth_token),
   path('logout/', LogoutView.as_view()),
   path('user/<int:id>', user_detail_api_view),
   path('<int:partner_id>/kaspi_xml', product_list_xml),
]
