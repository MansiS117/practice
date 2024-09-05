from django.contrib import admin
from .models import Category , Book  , Cart , CartItem

# Register your models here.
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug" : ("name" ,)}
#     list_display = ("name" , "slug")

admin.site.register(Category)
admin.site.register(Book)
# admin.site.register(Ratings)
admin.site.register(Cart)
admin.site.register(CartItem)
