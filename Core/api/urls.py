from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeDiscountViewSet, LogoutView, BucketViewSet, ProductViewSet, OrderViewSet, CreateCheck, \
    user_detail_api_view
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('time_discount', TimeDiscountViewSet)
router.register('bucket', BucketViewSet)
router.register('product', ProductViewSet)
router.register('order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('create-check/', CreateCheck.as_view(), name='create-check'),
    path('user/<int:id>', user_detail_api_view),
]
