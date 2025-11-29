from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Food, Bookmark, Visited


class RestaurantViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")

        cls.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            city="Test City",
            opening_time="09:00:00",
            closing_time="22:00:00",
            average_rating=4.2,
        )

        cls.food = Food.objects.create(
            name="Test Food",
            price=100,
            restaurant=cls.restaurant
        )

        cls.client = Client()

    def test_RestaurantListView(self):
        url = reverse("restaurants:restaurant_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/list.html")
        self.assertIn("restaurants", response.context)

    def test_RestaurantDetailView(self):
        url = reverse("restaurants:restaurant_detail", args=[self.restaurant.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/detail.html")
        self.assertEqual(response.context["restaurant"], self.restaurant)

    def test_FoodListView(self):
        url = reverse("restaurants:restaurant_foods", args=[self.restaurant.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "foods/list.html")
        self.assertIn("foods", response.context)
        self.assertEqual(response.context["restaurant"], self.restaurant)

    def test_toggle_bookmark(self):
        self.client.login(username="testuser", password="12345")

        url = reverse("restaurants:toggle_bookmark")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())

        response = self.client.post(url, {"restaurant_id": self.restaurant.id})
        self.assertFalse(Bookmark.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_toggle_visited(self):
        self.client.login(username="testuser", password="12345")

        url = reverse("restaurants:toggle_visited")
        response = self.client.post(url, {"restaurant_id": self.restaurant.id})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Visited.objects.filter(user=self.user, restaurant=self.restaurant).exists())

        response = self.client.post(url, {"restaurant_id": self.restaurant.id})
        self.assertFalse(Visited.objects.filter(user=self.user, restaurant=self.restaurant).exists())
