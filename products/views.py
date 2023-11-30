from rest_framework import mixins, viewsets

from products.models import DealerPrice
from products.serializers import DealerPriceSerializer


class DealerPriceViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    serializer_class = DealerPriceSerializer
    queryset = (DealerPrice.objects.
                select_related('dealer_id').
                prefetch_related('matches__product_id'))
