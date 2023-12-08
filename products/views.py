from django.db import connection
from django.db.models import Exists, OuterRef
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   extend_schema, inline_serializer)
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import IntegerField
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from ML.prediction_model import ProseptDescriptionSearcher

from .filters import DealerPriceFilter
from .models import DealerPrice, Product, ProductDealer
from .serializers import (DealerPriceSerializer, ProductDealerWriteSerializer,
                          ProductSerializer)

prediction_model = ProseptDescriptionSearcher(connection=connection)


class DealerPriceViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    serializer_class = DealerPriceSerializer
    queryset = (
        DealerPrice.objects
        .select_related('dealer')
        .prefetch_related('matches__product')
        .annotate(
            status=Exists(ProductDealer.objects.filter(
                key_id=OuterRef('pk'),
            ))
        )
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealerPriceFilter

    @extend_schema(
        responses={
            200: inline_serializer(
                name='StatiscticsResponse',
                fields={
                    'total': IntegerField(),
                    'marked': IntegerField(),
                    'unmarked': IntegerField(),
                }
            ),
        }
    )
    @action(detail=False,
            methods=('get',))
    def stats(self, request):
        total = DealerPrice.objects.count()
        marked = ProductDealer.objects.count()
        data = {
            'total': total,
            'marked': marked,
            'unmarked': total - marked
        }
        return Response(data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='quantity', description='Number of recommendations',
                type=int, default=5
            ),
        ],
        responses={
            200: OpenApiResponse(response=ProductSerializer)
        },
    )
    @action(detail=True,
            methods=('get',))
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
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    search_fields = ('name',)


class ProductDealerViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin):
    serializer_class = ProductDealerWriteSerializer
    queryset = ProductDealer.objects.select_related('product', 'key', 'dealer')
