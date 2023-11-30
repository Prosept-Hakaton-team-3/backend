from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Dealer, DealerPrice, Product, ProductDealer

# TODO: better admin panel
admin.site.register(Dealer)
admin.site.register(Product)
admin.site.register(ProductDealer)
admin.site.register(DealerPrice)
admin.site.unregister(Group)
