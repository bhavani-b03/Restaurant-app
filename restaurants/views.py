from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Food, Cuisine, Bookmark, Visited, Review
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.db.models import Count, Avg
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ReviewForm
from django.urls import reverse
# Create your views here.
DEFAULT_MIN_PRICE = 0
DEFAULT_MAX_PRICE = 100000

class RestaurantListView(ListView):
    model = Restaurant
    template_name = "restaurants/list.html"  
    context_object_name = "restaurants"  
    paginate_by = 10  

    ordering = ['-average_rating']
    
    def filter_price(self, qs):
        start = self.request.GET.get("start")
        end = self.request.GET.get("end")

        if start and end:
            return qs.filter(cost_for_two__gte=int(start), cost_for_two__lte=int(end))
        return qs    
    
    def apply_filters(self, qs):
        qs = self.filter_price(qs)
        return qs

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('images').with_user_bookmarks(self.request.user).with_user_visited(self.request.user)
        return self.apply_filters(qs)

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurants/detail.html"  
    context_object_name = "restaurant"

    def get_queryset(self):
        return super().get_queryset().prefetch_related('images', 'cuisines', 'reviews__user').with_user_visited(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = self.object.reviews.select_related('user').all()
        context["rating_stats"] = self.object.get_rating_stats()
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

class AddReviewView(LoginRequiredMixin, UpdateView):  
    model = Review
    template_name = "restaurants/detail.html"
    form_class = ReviewForm

    def get_object(self, queryset=None):
        self.restaurant = get_object_or_404(Restaurant, id=self.kwargs["restaurant_id"])
        review, created = Review.objects.get_or_create(
            user=self.request.user,
            restaurant=self.restaurant,
            defaults={"rating": 0, "comment": ""}
        )
        return review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["restaurant"] = self.restaurant
        return context

    def form_valid(self, form):
        review = form.save()
        review.restaurant.update_average_rating()
        return redirect("restaurants:restaurant_detail", pk=self.restaurant.id)

class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def test_func(self):
        return self.get_object().user == self.request.user

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        restaurant = self.object.restaurant  # save restaurant before deletion
        response = super().delete(request, *args, **kwargs)
        restaurant.update_average_rating()  # update after deletion
        return response

    def get_success_url(self):
        return reverse('restaurants:restaurant_detail', kwargs={'pk': self.object.restaurant.id})
