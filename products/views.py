import logging

from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from ML.prediction_model import ProseptDescriptionSearcher
from .models import DealerPrice, Product, ProductDealer
from .serializers import (DealerPriceSerializer, ProductDealerWriteSerializer,
                          ProductSerializer)

try:
    prediction_model = ProseptDescriptionSearcher()
except:
    logging.exception('Ошибка', exc_info=True)


class DealerPriceViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    serializer_class = DealerPriceSerializer
    queryset = (DealerPrice.objects.
                select_related('dealer').
                prefetch_related('matches__product'))

    # TODO: система статусов, показ всех вариантов модели (лучше по кнопке показать еще..)
    @action(detail=True,
            methods=('get',))
    # TODO: params to swagger
    def recommendations(self, request, pk):
        quantity = request.query_params.get('quantity', 5)
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response('Количество должно быть целым числом.',
                            status=HTTP_400_BAD_REQUEST)
        dealer_product = get_object_or_404(DealerPrice, id=pk)
        recommends = prediction_model.match_product({
            'target': model_to_dict(
                dealer_product,
                fields=['id', 'product_name', 'product_key']
            )},
            quantity
        )
        recommended_products = [
            get_object_or_404(Product, id=pk) for pk in recommends
        ]

        serializer = ProductSerializer(
            recommended_products, many=True
        )
        return Response(serializer.data, status=HTTP_200_OK)


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
    queryset = ProductDealer.objects.select_related('product', 'key', 'dealer')
