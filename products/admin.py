from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Dealer, DealerPrice, Product, ProductDealer


@admin.register(DealerPrice)
class DealerPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_key', 'product_name',
                    'product_url', 'date', 'dealer', 'get_status')
    list_filter = ('dealer', 'date')
    list_display_links = ('id', 'product_key',)
    search_fields = ('product_name', 'product_key',)

    @admin.display(description='Статус')
    def get_status(self, obj):
        return (
            'Размечен'
            if ProductDealer.objects.filter(key=obj).exists()
            else 'Не определен'
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'ean_13', 'name', 'category_id')
    list_filter = ('article', 'ean_13', 'category_id')
    list_display_links = ('id', 'article')
    search_fields = ('article', 'ean_13', 'name')


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(ProductDealer)
class ProductDealerAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'product', 'dealer')
    list_filter = ('key', 'product',)
    list_display_links = ('id', 'key',)
    search_fields = ('key',)


admin.site.unregister(Group)
