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

    class Meta:
        model = Restaurant
        fields = ['cost_for_two_min', 'cost_for_two_max', 'diet_type', 'cuisines']
