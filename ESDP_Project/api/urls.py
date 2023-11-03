from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeDiscountViewSet, LogoutView, BucketViewSet, ProductViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register('time_discount', TimeDiscountViewSet)
router.register('bucket', BucketViewSet)
router.register('product', ProductViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('login/', obtain_auth_token),
   path('logout/', LogoutView.as_view()),
]
