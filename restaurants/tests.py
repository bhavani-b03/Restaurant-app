from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Cuisine, Food, Bookmark, Visited
import datetime
from tests.mixins import UserMixin, RestaurantMixin, FoodMixin

class TestRestaurantListView(RestaurantMixin):
    def test_list_page_should_load_restaurants(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger King")

    def test_restaurant_list_should_filter_by_price_range(self):

        response = self.client.get(reverse("restaurants:restaurant_list") + "?max_price=500")
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger King")
        self.assertNotContains(response, "Fancy Feast")



class TestRestaurantDetailView(RestaurantMixin):
    def test_detail_page_should_display_correct_restaurant(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger King")


class TestFoodListView(FoodMixin):
    def test_food_list_should_show_related_food(self):
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fried Rice")


class TestToggleBookmark(RestaurantMixin):
    def test_user_should_toggle_bookmark_on(self):
        self.login()
        url = reverse("restaurants:toggle_bookmark")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        self.assertJSONEqual(response.content, {"bookmarked": True})

    def test_user_should_toggle_bookmark_off(self):
        self.login()
        Bookmark.objects.create(user=self.user, restaurant=self.restaurant)
        url = reverse("restaurants:toggle_bookmark")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        self.assertJSONEqual(response.content, {"bookmarked": False})


class TestToggleVisited(RestaurantMixin):
    def test_user_should_toggle_visited_on(self):
        self.login()
        url = reverse("restaurants:toggle_visited")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Visited.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        self.assertJSONEqual(response.content, {"visited": True})

    def test_user_should_toggle_visited_off(self):
        self.login()
        Visited.objects.create(user=self.user, restaurant=self.restaurant)
        url = reverse("restaurants:toggle_visited")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Visited.objects.filter(user=self.user, restaurant=self.restaurant).exists())
        self.assertJSONEqual(response.content, {"visited": False})
