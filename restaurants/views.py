from django.shortcuts import render
from .models import Restaurant
from django.views.generic import ListView

# Create your views here.

class RestaurantListView(ListView):
    model = Restaurant
    template_name = "restaurants/list.html"  
    context_object_name = "restaurants"  
    paginate_by = 10  

    ordering = ['-average_rating']

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('images')  # fetch images to avoid extra queries
        return qs
