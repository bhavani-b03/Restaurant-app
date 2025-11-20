from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Food, Cuisine
from django.views.generic import ListView, DetailView

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

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurants/detail.html"  
    context_object_name = "restaurant"

    def get_queryset(self):
        return super().get_queryset().prefetch_related('images', 'cuisines')
    
class FoodListView(ListView):
    model = Food
    template_name = "foods/list.html"
    context_object_name = "foods"

    def get_queryset(self):
        self.restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        return Food.objects.filter(restaurant=self.restaurant).prefetch_related('cuisines')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = self.restaurant
        return context
