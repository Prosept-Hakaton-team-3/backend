from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import Dealer, DealerPrice, Product, ProductDealer


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'article', 'name', 'ean_13', 'ozon_name', 'name_1c',
                  'wb_name', 'ozon_article', 'wb_article', 'ym_article',
                  'cost', 'recommended_price',)


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'article', 'name', 'ean_13')


class ProductDealerReadSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer()

    class Meta:
        model = ProductDealer
        fields = ('id', 'product',)


class ProductDealerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDealer
        fields = ('id', 'product', 'dealer', 'key')

    def validate(self, attrs):
        if ProductDealer.objects.filter(dealer=attrs.get('dealer'),
                                        product=attrs.get('product'),
                                        key=attrs.get('key')
                                        ).exists():
            raise ValidationError('Эти продукты уже сопоставлены')
        return attrs


class DealerPriceSerializer(serializers.ModelSerializer):
    dealer = DealerSerializer()
    matches = ProductDealerReadSerializer(many=True)
    status = serializers.BooleanField(default=0)

    class Meta:
        model = DealerPrice
        fields = ('id', 'product_key', 'product_name', 'price',
                  'product_url', 'date', 'dealer', 'status', 'matches',)
