from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Food, Cuisine, Bookmark, Visited, Review
from django.views.generic import ListView, DetailView
from django.db.models import Count

# Create your views here.

class RestaurantListView(ListView):
    model = Restaurant
    template_name = "restaurants/list.html"  
    context_object_name = "restaurants"  
    paginate_by = 10  

    ordering = ['-average_rating']

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('images').with_user_bookmarks(self.request.user).with_user_visited(self.request.user)
        return qs

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurants/detail.html"  
    context_object_name = "restaurant"

    def get_queryset(self):
        return super().get_queryset().prefetch_related('images', 'cuisines').with_user_visited(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.object

        rating_counts = restaurant.reviews.values('rating').annotate(count=Count('rating'))

        rating_data = {str(i): 0 for i in range(1, 6)}
        for r in rating_counts:
            rating_data[str(r['rating'])] = r['count']

        total = sum(rating_data.values()) or 1
        rating_percentage = {
            star: round((count / total) * 100)
            for star, count in rating_data.items()
        }

        # ⭐ Make a combined list for direct looping in template
        rating_stats = [
            {
                "star": star,
                "percentage": rating_percentage[star],
                "count": rating_data[star],
            }
            for star in ["5", "4", "3", "2", "1"]
        ]

        context["rating_stats"] = rating_stats
        return context

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

@require_POST
@login_required
def toggle_visited(request):
    restaurant_id = request.POST.get("restaurant_id")
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except (TypeError, ValueError, Restaurant.DoesNotExist):
        return JsonResponse({"error": "Invalid restaurant ID"}, status=400)

    visited, created = Visited.objects.get_or_create(
        user=request.user,
        restaurant=restaurant
    )

    if not created:
        visited.delete()
        return JsonResponse({"visited": False})

    return JsonResponse({"visited": True})

@login_required
def add_review(request):
    restaurant = Restaurant.objects.get(id=request.POST.get("restaurant_id"))
    Review.objects.create(
        user=request.user,
        restaurant=restaurant,
        rating=request.POST.get("rating"),
        comment=request.POST.get("comment"),
    )
    return JsonResponse({"success": True})
