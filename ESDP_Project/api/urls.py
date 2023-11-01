from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeDiscountViewSet, LogoutView, BucketViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register('time_discount', TimeDiscountViewSet)
router.register('bucket', BucketViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('login/', obtain_auth_token),
   path('logout/', LogoutView.as_view()),
]
