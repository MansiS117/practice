from django.db import models
from django.contrib.auth.models  import User 

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length= 100)
    slug = models.SlugField(max_length=100 , unique= True , null = True)
    # cat_image = models.ImageField(upload_to= "media/categories" , blank = True)
        


    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length= 100 , blank = False)
    author = models.CharField(max_length=50)
    category = models.ForeignKey(Category , on_delete= models.SET_NULL , null = True) 
    price =  models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to= "media" , null = True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add= True , blank = True , null = True) 
    modified = models.DateTimeField(auto_now= True)
    is_available = models.BooleanField(default= True)


    def __str__(self):
        return self.title
    


class Ratings(models.Model):
    book = models.ForeignKey(Book , on_delete= models.CASCADE)
    user = models.ForeignKey(User , on_delete= models.CASCADE )
    rating = models.PositiveIntegerField()
    

# class cart(models.Models):
