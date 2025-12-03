from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .managers import RestaurantQuerySet
from django.db.models import Count, Avg

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.name


class DietType(models.IntegerChoices):
    VEG = 1, 'Vegetarian'
    NON_VEG = 2, 'Non-Vegetarian'
    VEGAN = 3, 'Vegan'


class Restaurant(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)  
    city = models.CharField(max_length=100)
    address = models.TextField()
    cost_for_two = models.IntegerField(default=0)
    diet_type = models.IntegerField(choices=DietType.choices, default=DietType.VEG)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_spotlight = models.BooleanField(default=False)
    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants', blank=True)  # A restaurant may start without cuisines

    objects = RestaurantQuerySet.as_manager()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("restaurants:restaurant_detail", kwargs={"pk": self.pk})
    
    def get_foods_url(self):
        return reverse("restaurants:restaurant_foods", kwargs={"restaurant_id": self.pk})
    
    def update_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.average_rating = round(avg, 1)
        else:
            self.average_rating = 0.0
        self.save()

    def get_rating_stats(self):
        rating_counts = self.reviews.values('rating').annotate(count=Count('rating'))

        rating_data = {str(i): 0 for i in range(1, 6)}
        for item in rating_counts:
            rating_data[str(item['rating'])] = item['count']

        total_reviews = sum(rating_data.values()) or 1  # avoid divide by zero
        rating_percentage = {
            star: round((count / total_reviews) * 100)
            for star, count in rating_data.items()
        }

        rating_stats = [
            {"star": star, "percentage": rating_percentage[star], "count": rating_data[star]}
            for star in ["5", "4", "3", "2", "1"]
        ]
        return rating_stats


class Food(TimeStampedModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu')
    name = models.CharField(max_length=200)  
    price = models.DecimalField(max_digits=8, decimal_places=2)
    diet_type = models.IntegerField(choices=DietType.choices, default=DietType.VEG)
    description = models.TextField(blank=True, null=True)  
    cuisines = models.ManyToManyField(Cuisine, related_name='foods', blank=True)  
    image = models.ImageField(upload_to="food_images/%Y/%m/%d/", blank=True, null=True)
    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="restaurant_images/")  


class Review(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()  
    comment = models.TextField(blank=True)  

    class Meta:
        unique_together = ('user', 'restaurant')  

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} - {self.rating}"


class Bookmark(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookmarked_by')

    class Meta:
        unique_together = ('user', 'restaurant')  

    def __str__(self):
        return f"{self.user.username} bookmarked {self.restaurant.name}"


class Visited(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visited_restaurants')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='visited_by')

    class Meta:
        unique_together = ('user', 'restaurant')  

    def __str__(self):
        return f"{self.user.username} visited {self.restaurant.name}"
