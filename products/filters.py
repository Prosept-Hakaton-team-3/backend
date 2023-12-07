from django_filters import BooleanFilter, CharFilter, FilterSet

from .models import DealerPrice


class DealerPriceFilter(FilterSet):
    status = BooleanFilter()
    dealer = CharFilter(field_name='dealer__name', lookup_expr='iexact')

    class Meta:
        model = DealerPrice
        fields = ('dealer', 'date', 'status')
