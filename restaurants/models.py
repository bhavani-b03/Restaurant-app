from django.db import models
from django.contrib.auth.models import User


class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
   

class Restaurant(models.Model):
    VEG_CHOICES = [
        ('veg', 'Vegetarian'),
        ('nonveg', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
    ]

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    cost_for_two = models.IntegerField()
    veg_type = models.CharField(max_length=10, choices=VEG_CHOICES)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_spotlight = models.BooleanField(default=False)
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)

    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants')


    def __str__(self):
        return self.name
    


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'restaurant')  # ensures one review per user per restaurant

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} - {self.rating}"



class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')  # ensures no duplicate bookmarks

    def __str__(self):
        return f"{self.user.username} bookmarked {self.restaurant.name}"



class Visited(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visited_restaurants')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='visited_by')
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')  # ensures one visit per user per restaurant

    def __str__(self):
        return f"{self.user.username} visited {self.restaurant.name}"


