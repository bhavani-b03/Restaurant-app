from django.urls import reverse
from django.test import TestCase
from .models import Bookmark, Visited
from restaurants.test_restaurants.mixins import RestaurantTestSetupMixin

class TestRestaurantListView(RestaurantTestSetupMixin, TestCase):
    def test_list_page_should_load_restaurants(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertEqual(response.status_code, 200)

    def test_all_restaurants_should_be_listed(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))

        self.assertContains(response, self.restaurant.name)

    def test_restaurant_should_link_to_correct_detail_page(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertContains(response, self.restaurant.get_absolute_url())


class TestRestaurantDetailView(RestaurantTestSetupMixin, TestCase):
    def test_detail_page_should_display_correct_restaurant(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)


class TestFoodListView(RestaurantTestSetupMixin, TestCase):
    def test_food_list_should_show_related_food(self):
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_all_food_items_should_be_displayed(self):
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)
        self.assertContains(response, self.food.name)


class TestToggleBookmark(RestaurantTestSetupMixin, TestCase):
    def test_user_should_toggle_bookmark_on(self):
        url = reverse("restaurants:toggle_bookmark")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists()
        )
        self.assertJSONEqual(response.content, {"bookmarked": True})

    def test_user_should_toggle_bookmark_off(self):
        Bookmark.objects.create(user=self.user, restaurant=self.restaurant)

        url = reverse("restaurants:toggle_bookmark")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists()
        )
        self.assertJSONEqual(response.content, {"bookmarked": False})


class TestToggleVisited(RestaurantTestSetupMixin, TestCase):
    def test_user_should_toggle_visited_on(self):
        url = reverse("restaurants:toggle_visited")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Visited.objects.filter(user=self.user, restaurant=self.restaurant).exists()
        )
        self.assertJSONEqual(response.content, {"visited": True})

    def test_user_should_toggle_visited_off(self):
        Visited.objects.create(user=self.user, restaurant=self.restaurant)

        url = reverse("restaurants:toggle_visited")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Visited.objects.filter(user=self.user, restaurant=self.restaurant).exists()
        )
        self.assertJSONEqual(response.content, {"visited": False})
