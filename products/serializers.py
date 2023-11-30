from rest_framework import serializers

from products.models import Dealer, DealerPrice, Product, ProductDealer


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'ean_13',)


class ProductDealerSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()

    class Meta:
        model = ProductDealer
        fields = ('product_id',)


class DealerPriceSerializer(serializers.ModelSerializer):
    dealer_id = DealerSerializer()
    matches = ProductDealerSerializer(many=True)

    class Meta:
        model = DealerPrice
        fields = ('id', 'product_key', 'product_name',
                  'date', 'dealer_id', 'matches')
