import django_filters
from .models import Restaurant

class RestaurantFilter(django_filters.FilterSet):

    cost_for_two_min = django_filters.NumberFilter(field_name="cost_for_two", lookup_expr="gte")
    cost_for_two_max = django_filters.NumberFilter(field_name="cost_for_two", lookup_expr="lte")

    class Meta:
        model = Restaurant
        fields = ['cost_for_two_min', 'cost_for_two_max']
