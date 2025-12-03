from django.test import TestCase
from django.contrib.auth import get_user_model
from .factories import (
    UserFactory,
    RestaurantFactory,
    FoodFactory,
    CuisineFactory,
    ReviewFactory,
    BookmarkFactory,
    VisitedFactory,
)

User = get_user_model()


class AuthMixin(TestCase):
    def create_user(self, **kwargs):
        self.user = UserFactory(**kwargs)
        return self.user

    def login_user(self, user=None):
        if not user:
            user = self.create_user()

        self.client.login(username=user.username, password="pass123")
        return user


class RestaurantTestSetupMixin(AuthMixin):
    def setUp(self):
        super().setUp()
        
        self.user = self.create_user()
        self.login_user(self.user)

        self.cuisine = CuisineFactory()

        self.restaurant = RestaurantFactory(cuisines=[self.cuisine])

        self.food = FoodFactory(restaurant=self.restaurant, cuisines=[self.cuisine])

        self.cuisines = [CuisineFactory(name="Italian"), CuisineFactory(name="Chinese")]
        
        self.restaurants = []

        for i in range(5):  
            assigned_cuisines = self.cuisines[:i % 2 + 1]  # simple pattern for example
            restaurant = RestaurantFactory(cuisines=assigned_cuisines)
            self.restaurants.append(restaurant)

            FoodFactory(restaurant=restaurant, cuisines=assigned_cuisines)

