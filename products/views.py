from rest_framework import mixins, viewsets

from products.models import DealerPrice, Product, ProductDealer
from products.serializers import (DealerPriceSerializer,
                                  ProductDealerWriteSerializer,
                                  ProductSerializer)


class DealerPriceViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    serializer_class = DealerPriceSerializer
    queryset = (DealerPrice.objects.
                select_related('dealer').
                prefetch_related('matches__product'))


class ProductViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    search_fields = ('name',)


class ProductDealerViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    serializer_class = ProductDealerWriteSerializer
    queryset = ProductDealer.objects.all()

