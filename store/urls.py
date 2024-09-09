from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import BookDetailView, HomeView ,CategoryDetailView , RegistrationView , LoginView , AddToCartView , CartView, QuantityView, RemoveView


urlpatterns = [
   
    path("" ,HomeView.as_view(), name = "home"),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path("details/<int:book_id>/" , BookDetailView.as_view() , name = "book_detail"),
    path('cart' , CartView.as_view() , name = 'cart'),
    path('addtocart/<int:book_id>/', AddToCartView.as_view(),name='add_to_cart'),
    path('cart/quantity/', QuantityView.as_view(), name="quantity_item"),
    path('cart/remove/<int:item_id>/', RemoveView.as_view(), name="remove_item"),
    path('search' , views.search , name = 'search'),
    path('register/' , RegistrationView.as_view(), name = "register"),
    path("login/" , LoginView.as_view(), name = "login"),
    path("logout" , views.user_logout , name = "logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)