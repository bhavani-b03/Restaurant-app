from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Food, Cuisine, Bookmark
from django.views.generic import ListView, DetailView

# Create your views here.

class RestaurantListView(ListView):
    model = Restaurant
    template_name = "restaurants/list.html"  
    context_object_name = "restaurants"  
    paginate_by = 10  

    ordering = ['-average_rating']

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('images').with_user_bookmarks(self.request.user)
        return qs

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurants/detail.html"  
    context_object_name = "restaurant"

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('images', 'cuisines')
        return qs 

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

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Bookmark, Restaurant

@require_POST
@login_required
def toggle_bookmark(request):
    restaurant_id = request.POST.get("restaurant_id")
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except (Restaurant.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"error": "Invalid restaurant ID"}, status=400)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        restaurant=restaurant
    )

    if not created:
        bookmark.delete()
        return JsonResponse({"bookmarked": False})

    return JsonResponse({"bookmarked": True})
