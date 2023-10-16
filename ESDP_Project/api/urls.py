from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeDiscountViewSet


router = DefaultRouter()
router.register('time_discount', TimeDiscountViewSet)

urlpatterns = [
   path('', include(router.urls))
]
