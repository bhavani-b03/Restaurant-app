import django_filters
from django import forms
from .models import Restaurant, DietType

CUSTOM_DIET_CHOICES = [
    (1, "Veg"),       
    (2, "Non Veg"),
    (3, "Vegan")   
]
class RestaurantFilter(django_filters.FilterSet):

    cost_for_two_min = django_filters.NumberFilter(field_name="cost_for_two", lookup_expr="gte")
    cost_for_two_max = django_filters.NumberFilter(field_name="cost_for_two", lookup_expr="lte")

    diet_type = django_filters.MultipleChoiceFilter(
        choices=CUSTOM_DIET_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Restaurant
        fields = ['cost_for_two_min', 'cost_for_two_max', 'diet_type']
