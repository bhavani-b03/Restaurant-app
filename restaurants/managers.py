from django.db import models
from django.db.models import Exists, OuterRef, Value, BooleanField 

class RestaurantQuerySet(models.QuerySet):
    def with_user_bookmarks(self, user):
        from .models import Bookmark
        if user.is_authenticated:
            user_bookmarks = Bookmark.objects.filter(
                user=user,
                restaurant=OuterRef('pk')
            )
            return self.annotate(
                is_bookmarked=Exists(user_bookmarks)
            )
        return self.annotate(
            is_bookmarked=Value(False, output_field=BooleanField()))
