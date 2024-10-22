# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from .models import Profile
from .views import HomeView  # Import HomeView


class BannedBooksMiddleware(MiddlewareMixin):
    banned_books = {
        "India": [10],
        "Canada": [3],
        # Add more countries and banned book IDs as needed
    }

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check if the view function is from HomeView
        if (
            hasattr(view_func, "view_class")
            and view_func.view_class == HomeView
        ):
            # Initialize banned_book_ids as empty
            banned_book_ids = []

            if request.user.is_authenticated:
                # Use filter to check for profile existence
                profile = Profile.objects.filter(user=request.user).first()

                if profile:
                    country = profile.country
                    banned_book_ids = self.banned_books.get(country, [])

            # Set banned_book_ids in kwargs for HomeView
            view_kwargs["banned_book_ids"] = banned_book_ids
        return None
