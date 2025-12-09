import django_filters
from django import forms
from .models import Restaurant, DietType, Cuisine
class RestaurantFilter(django_filters.FilterSet):

    cost_for_two_min = django_filters.NumberFilter(field_name="cost_for_two", lookup_expr="gte")
    cost_for_two_max = django_filters.NumberFilter(field_name="cost_for_two", lookup_expr="lte")

    diet_type = django_filters.MultipleChoiceFilter(
        choices=DietType.choices,
        widget=forms.CheckboxSelectMultiple
    )

    cuisines = django_filters.ModelMultipleChoiceFilter(
        queryset=Cuisine.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    rating = django_filters.MultipleChoiceFilter(
        field_name="average_rating",
        choices=[(n, n) for n in range(1, 6)],  # 1 to 5 stars
        lookup_expr="exact"
    )

    is_spotlight = django_filters.BooleanFilter(field_name="is_spotlight")
    
    sort_by = django_filters.ChoiceFilter(
        method="sort_by_price",
        choices=[
            ('price_low', 'Low → High'),
            ('price_high', 'High → Low'),
        ],
        empty_label=None
    )

    sort_by_rating = django_filters.ChoiceFilter(
        method="sort_by_ratings",
        choices=[
            ('rating_high', 'High → Low'),
            ('rating_low', 'Low → High'),
        ],
        empty_label=None
    )
    
    search = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search')

    class Meta:
        model = Restaurant
        fields = ['cost_for_two_min', 'cost_for_two_max', 'diet_type', 'cuisines', 'rating', 'is_spotlight', 'search']

    def sort_by_price(self, queryset, name, value):
        if value == "price_low":
            return queryset.order_by("cost_for_two")
        if value == "price_high":
            return queryset.order_by("-cost_for_two")
        return queryset

    def sort_by_ratings(self, queryset, name, value):
        if value == "rating_high":
            return queryset.order_by("-average_rating")
        if value == "rating_low":
            return queryset.order_by("average_rating")
        return queryset

