from django.contrib import admin
from .models import Category , Book  , Cart , CartItem , User
from django.contrib.auth.admin import UserAdmin



class MyUserAdmin(UserAdmin):
    list_display = ("email" , "first_name" , "last_name" , "user_type","last_login" , "date_joined" , "is_active") #display this fields in the admin site
    list_display_links = ("email" , "first_name" , "last_name") # can see the details of user by clicking on this fields 
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ("email" ,)

admin.site.register(Category)
admin.site.register(Book)
# admin.site.register(Ratings)  
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(User , MyUserAdmin)