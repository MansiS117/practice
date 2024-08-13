from django.contrib import admin
from .models import Category , Book ,Ratings

# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Ratings)
