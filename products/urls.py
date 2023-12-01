from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import DealerPriceViewSet

v1_product_router = DefaultRouter()
v1_product_router.register('products', DealerPriceViewSet, basename='products')

urlpatterns = [
    path('', include(v1_product_router.urls))
]
