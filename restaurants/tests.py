from django.urls import reverse
from django.test import TestCase
from .models import Bookmark, Visited, Review
from restaurants.test_restaurants.mixins import RestaurantTestSetupMixin
from django.contrib.auth.models import User

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

    def test_price_filter_should_include_restaurants_within_range(self):
        response = self.client.get(
            reverse("restaurants:restaurant_list") + "?cost_for_two_min=100&cost_for_two_max=300"
        )
        included = [r for r in self.restaurants if 100 <= r.cost_for_two <= 300]
        for r in included:
            self.assertContains(response, r.name)

    def test_price_filter_should_exclude_restaurants_outside_range(self):
        response = self.client.get(
            reverse("restaurants:restaurant_list") + "?cost_for_two_min=100&cost_for_two_max=300"
        )
        excluded = [r for r in self.restaurants if r.cost_for_two < 100 or r.cost_for_two > 300]
        for r in excluded:
            self.assertNotContains(response, r.name)

    def test_diet_type_filter_should_include_selected_types(self):
        response = self.client.get(reverse("restaurants:restaurant_list") + "?diet_type=1")
        included = [r for r in self.restaurants if r.diet_type == 1]
        for r in included:
            self.assertContains(response, r.name)

    def test_diet_type_filter_should_exclude_unselected_types(self):
        response = self.client.get(reverse("restaurants:restaurant_list") + "?diet_type=1")
        excluded = [r for r in self.restaurants if r.diet_type != 1]
        for r in excluded:
            self.assertNotContains(response, r.name)

    def test_cuisine_filter_should_include_selected_cuisines(self):
        response = self.client.get(reverse("restaurants:restaurant_list") + "?cuisines=1")
        included = [r for r in self.restaurants if r.cuisines.filter(id=1).exists()]
        for r in included:
            self.assertContains(response, r.name)

    def test_cuisine_filter_should_exclude_unselected_cuisines(self):
        response = self.client.get(reverse("restaurants:restaurant_list") + "?cuisines=1")
        excluded = [r for r in self.restaurants if not r.cuisines.filter(id=1).exists()]
        for r in excluded:
            self.assertNotContains(response, r.name)

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

class TestAddReviewView(RestaurantTestSetupMixin):
    def test_should_create_new_review_if_none_exists(self):
        url = reverse("restaurants:add_review", kwargs={"restaurant_id": self.restaurant.id})
        response = self.client.post(url, {"rating": 5, "comment": "Amazing food!", "restaurant_id": self.restaurant.id})
        self.assertEqual(response.status_code, 302)
        review = Review.objects.get(user=self.user, restaurant=self.restaurant)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Amazing food!")

    def test_should_update_existing_review(self):
        Review.objects.create(user=self.user, restaurant=self.restaurant, rating=3, comment="Good")
        url = reverse("restaurants:add_review", kwargs={"restaurant_id": self.restaurant.id})
        self.client.post(url, {"rating": 4, "comment": "Better now", "restaurant_id": self.restaurant.id})
        review = Review.objects.get(user=self.user, restaurant=self.restaurant)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Better now")


    def test_should_require_login(self):
        self.client.logout()
        url = reverse("restaurants:add_review", kwargs={"restaurant_id": self.restaurant.id})
        response = self.client.post(url, {"rating": 5, "comment": "Test"})
        self.assertRedirects(response, f"/accounts/login/?next={url}")

class TestDeleteReviewView(RestaurantTestSetupMixin):
    def test_user_can_delete_own_review(self):
        review = Review.objects.create(user=self.user, restaurant=self.restaurant, rating=4, comment="Nice")
        url = reverse("restaurants:delete_review", kwargs={"pk": review.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_should_require_login(self):
        review = Review.objects.create(user=self.user, restaurant=self.restaurant, rating=4, comment="Nice")
        self.client.logout()
        url = reverse("restaurants:delete_review", kwargs={"pk": review.id})
        response = self.client.post(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_user_should_not_delete_others_review(self):
        other_user = User.objects.create_user(username="other", password="pass123")
        review_by_other = Review.objects.create(user=other_user, restaurant=self.restaurant, rating=5, comment="Great!")
        url = reverse("restaurants:delete_review", kwargs={"pk": review_by_other.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Review.objects.filter(id=review_by_other.id).exists())
