from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Cuisine, Food, Bookmark, Visited
import datetime
from tests.mixins import UserMixin, RestaurantMixin, FoodMixin
from django.template.defaultfilters import time as django_time

class TestRestaurantListView(RestaurantMixin):
    def test_list_page_should_load_restaurants(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertEqual(response.status_code, 200)

    def test_all_restaurants_are_listed(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))

        for restaurant in self.restaurants:
            self.assertContains(response, restaurant.name)

    def test_restaurant_links_to_correct_detail_page(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))

        for restaurant in self.restaurants:
            self.assertContains(response, restaurant.get_absolute_url())

    def test_page_contains_filter_buttons(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertContains(response, 'id="visitedFilterBtn"')
        self.assertContains(response, 'id="bookmarkFilterBtn"')


class TestRestaurantDetailView(RestaurantMixin):
    def test_detail_page_should_display_correct_restaurant(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger King")
    
    def test_detail_page_should_show_diet_type(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertContains(response, self.restaurant.diet_type)

    def test_detail_page_should_show_address(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertContains(response, self.restaurant.address)

    def test_detail_page_should_format_opening_and_closing_time(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        formatted_open = django_time(self.restaurant.opening_time, "g:i A")
        formatted_close = django_time(self.restaurant.closing_time, "g:i A")

        self.assertContains(response, formatted_open)
        self.assertContains(response, formatted_close)

    def test_detail_page_should_show_cuisines(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        for cuisine in self.restaurant.cuisines.all():
            self.assertContains(response, cuisine.name)

    def test_detail_page_should_show_cost_for_two(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertContains(response, f"₹{self.restaurant.cost_for_two}")

    def test_detail_page_should_show_images_if_exist(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertContains(response, "<img", html=False)

    def test_detail_page_should_show_no_image_message_when_empty(self):
        self.restaurant.images.all().delete()
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)
        self.assertContains(response, "No images available.")

    def test_detail_page_should_show_view_menu_button(self):
        url = reverse("restaurants:restaurant_detail", kwargs={"pk": self.restaurant.pk})
        response = self.client.get(url)

        expected_url = self.restaurant.get_foods_url()
        self.assertContains(response, f'href="{expected_url}"')


class TestFoodListView(FoodMixin):
    def test_food_list_should_show_related_food(self):
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_page_displays_restaurant_name(self):
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)
        self.assertContains(response, self.restaurant.name)

    def test_all_food_items_are_displayed(self):
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)

        for food in self.restaurant.menu.all():
            self.assertContains(response, food.name)

    def test_food_with_image_displays_image(self):
        food = self.restaurant.menu.first()
        
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)

        if food.image:
            self.assertContains(response, food.image.url)

    def test_price_displayed_with_currency_symbol(self):
        url = reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)

        for food in self.restaurant.menu.all():
            self.assertContains(response, f"₹{food.price}")


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
