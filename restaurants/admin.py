from django.contrib import admin

# Register your models here.
from .models import * 

admin.site.register(Cuisine)
admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(RestaurantImage)
admin.site.register(Review)
admin.site.register(Bookmark)
admin.site.register(Visited)
