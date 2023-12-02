from rest_framework import serializers

from products.models import Dealer, DealerPrice, Product, ProductDealer


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'article', 'name', 'ean_13', 'ozon_name', 'name_1c',
                  'wb_name', 'ozon_article', 'wb_article', 'ym_article',
                  'cost', 'min_recommended_price', 'recommended_price',)


class ProductDealerReadSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()

    class Meta:
        model = ProductDealer
        fields = ('id', 'product_id',)


class ProductDealerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDealer
        fields = ('id', 'product_id', 'dealer_id', 'key')


class DealerPriceSerializer(serializers.ModelSerializer):
    dealer_id = DealerSerializer()
    matches = ProductDealerReadSerializer(many=True)

    class Meta:
        model = DealerPrice
        fields = ('id', 'product_key', 'product_name', 'price',
                  'product_url', 'date', 'dealer_id', 'matches',)
