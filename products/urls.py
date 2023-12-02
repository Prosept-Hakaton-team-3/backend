from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import (DealerPriceViewSet, ProductDealerViewSet,
                            ProductViewSet)

v1_product_router = DefaultRouter()
v1_product_router.register(
    'products', DealerPriceViewSet, basename='products')
v1_product_router.register(
    'own-products', ProductViewSet, basename='own_products')
v1_product_router.register(
    'matches', ProductDealerViewSet, basename='matches')

urlpatterns = [
    path('', include(v1_product_router.urls))
]
