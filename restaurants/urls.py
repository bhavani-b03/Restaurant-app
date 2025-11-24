from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [
    path("", views.RestaurantListView.as_view(), name="restaurant_list"),
    path("<int:pk>/", views.RestaurantDetailView.as_view(), name="restaurant_detail"),
    path("<int:restaurant_id>/foods/", views.FoodListView.as_view(), name="restaurant_foods"),
    path("bookmark/toggle/", views.toggle_bookmark, name="toggle_bookmark"),
    path("visited/toggle/", views.toggle_visited, name="toggle_visited"),
    path("add-review/", views.add_review, name="add_review"),
]
