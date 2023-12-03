from rest_framework import serializers

from products.models import Dealer, DealerPrice, Product, ProductDealer


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'article', 'name', 'ean_13',)


class ProductDealerSerializer(serializers.ModelSerializer):
    dealer = DealerSerializer()
    product = ProductSerializer()

    class Meta:
        model = ProductDealer
        fields = ('dealer', 'product',)


class DealerPriceSerializer(serializers.ModelSerializer):
    dealer = DealerSerializer()
    matches = ProductDealerSerializer(many=True)

    class Meta:
        model = DealerPrice
        fields = ('id', 'product_key', 'product_name',
                  'date', 'dealer', 'matches')
