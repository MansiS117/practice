from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomManager
from django.utils import timezone

# Create your models here.


class TimestampModel(models.Model):
    created = models.DateTimeField(
        default=timezone.now, editable=False
    )  # Automatically set when created
    updated_at = models.DateTimeField(
        default=timezone.now, editable=False
    )  # Automatically set when updated

    class Meta:
        abstract = True


class Category(TimestampModel):
    name = models.CharField(max_length=100)
    # slug = models.SlugField(max_length=100 , unique= True , null = True)
    # cat_image = models.ImageField(upload_to= "media/categories" , blank = True)

    def __str__(self):
        return self.name


USER_TYPE_CHOICES = [
    ("buyer", "Buyer"),
    ("seller", "Seller"),
]


class User(AbstractUser, TimestampModel):
    username = None
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    email = models.EmailField(unique=True)

    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="buyer"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomManager()

    def __str__(self):
        return self.email


class Book(TimestampModel):
    title = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length=50)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="media", null=True)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def stock_status(self):
        if self.stock == 1:
            return "Only 1 left"
        elif self.stock > 1:
            return "Available in stock"
        else:
            return "Out of stock"


class Cart(TimestampModel):

    buyer = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return str(self.buyer) if self.buyer else "No Buyer"


class CartItem(TimestampModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.book.title


class Order(TimestampModel):
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    ordered_at = models.DateTimeField(
        auto_now_add=True
    )  # Total price of the order

    def __str__(self):
        return f"{self.buyer} "


class OrderItem(TimestampModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )  # Link to the order
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE
    )  # Link to the book
    quantity = models.PositiveIntegerField()  # Number of copies ordered
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Price per copy

    def __str__(self):
        return f"{self.quantity} x {self.book.title} by {self.order}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price


class Profile(TimestampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.user.email


# class Ratings(models.Model):
#     book = models.ForeignKey(Book , on_delete= models.CASCADE)
#     user = models.ForeignKey(User , on_delete= models.CASCADE )
#     rating = models.PositiveIntegerField()
