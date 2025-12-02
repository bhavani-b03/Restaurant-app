import factory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from restaurants.models import (
    Cuisine, Restaurant, Food, DietType, RestaurantImage, Review, Bookmark, Visited
)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "pass123")


class CuisineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cuisine

    name = factory.Sequence(lambda n: f"Cuisine {n}")


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.Sequence(lambda n: f"Restaurant {n}")
    city = factory.Faker("city")
    address = factory.Faker("address")
    cost_for_two = 400
    diet_type = DietType.VEG
    average_rating = 4.5
    opening_time = "09:00"
    closing_time = "22:00"
    is_spotlight = False

    @factory.post_generation
    def cuisines(self, create, extracted, **kwargs):
        # If caller passes cuisines, assign them
        if create and extracted:
            self.cuisines.set(extracted)
        # Default: add one cuisine if none passed
        elif create and not extracted:
            self.cuisines.add(CuisineFactory())


class RestaurantImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RestaurantImage

    restaurant = factory.SubFactory(RestaurantFactory)
    image = SimpleUploadedFile("test.jpg", b"fake content", content_type="image/jpeg")


class FoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Food

    restaurant = factory.SubFactory(RestaurantFactory)
    name = factory.Sequence(lambda n: f"Food {n}")
    price = 150
    diet_type = DietType.VEG
    description = factory.Faker("sentence")

    @factory.post_generation
    def cuisines(self, create, extracted, **kwargs):
        if create and extracted:
            self.cuisines.set(extracted)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(UserFactory)
    restaurant = factory.SubFactory(RestaurantFactory)
    rating = factory.Faker("random_int", min=1, max=5)
    comment = factory.Faker("sentence")


class BookmarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bookmark

    user = factory.SubFactory(UserFactory)
    restaurant = factory.SubFactory(RestaurantFactory)


class VisitedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Visited

    user = factory.SubFactory(UserFactory)
    restaurant = factory.SubFactory(RestaurantFactory)
