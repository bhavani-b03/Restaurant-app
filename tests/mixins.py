import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from restaurants.models import Restaurant, Cuisine, Food
from django.core.files.uploadedfile import SimpleUploadedFile

# -----------------------------
# User setup mixin
# -----------------------------
class UserMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="pass123",
            email="testuser@example.com"  # needed for password reset tests
        )
        super().setUpTestData()

    def login(self):
        self.client.login(username="testuser", password="pass123")


# -----------------------------
# Restaurant setup mixin
# -----------------------------
class RestaurantMixin(UserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()  # ensures UserMixin is applied

        # Sample cuisine
        cls.cuisine = Cuisine.objects.create(name="Indian")

        # Sample restaurant
        cls.restaurants = [
            Restaurant.objects.create(
            name="Burger King",
            address="Street 1",
            diet_type=1,  # integer for DietType choices
            average_rating=4.5,
            cost_for_two=400,
            opening_time=datetime.time(9, 0),
            closing_time=datetime.time(22, 0)
        )]
        cls.restaurant = cls.restaurants[0]
        cls.restaurant.cuisines.add(cls.cuisine)
        img = SimpleUploadedFile("test.jpg", b"fake-image-content", content_type="image/jpeg")
        cls.restaurant.images.create(image=img)


# -----------------------------
# Food setup mixin
# -----------------------------
class FoodMixin(RestaurantMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()  # ensures RestaurantMixin is applied

        # Sample food
        cls.food = Food.objects.create(
            restaurant=cls.restaurant,
            name="Fried Rice",
            price=150,
            diet_type=1
        )
