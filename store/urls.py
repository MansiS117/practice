from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import UpdateBook,OrderView, ReceivedOrdersView, RemoveBook, BookDetailView, HomeView, ProfileView ,AddBook, CategoryDetailView , RegistrationView , LoginView , SearchView , AddToCartView,  CartView, QuantityView, RemoveView


urlpatterns = [
   
    path("" ,HomeView.as_view(), name = "home"),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path("details/<int:book_id>/" , BookDetailView.as_view() , name = "book_detail"),
    path('cart' , CartView.as_view() , name = 'cart'),
    path('addtocart/<int:book_id>/', AddToCartView.as_view(),name='add_to_cart'),
    path('cart/quantity/', QuantityView.as_view(), name="quantity_item"),
    path('cart/remove/<int:item_id>/', RemoveView.as_view(), name="remove_item"),
    path('search' , SearchView.as_view() , name = 'search'),
    path('register/' , RegistrationView.as_view(), name = "register"),
    path("login/" , LoginView.as_view(), name = "login"),
    path("logout" , views.user_logout , name = "logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('order/', OrderView.as_view(), name="order"),
    path('checkout/', views.checkout, name= "checkout"),
    path('update_profile/', ProfileView.as_view(), name="profile"),
    path('add_book/', AddBook.as_view(), name="new_book"),
    path('update_book/<int:book_id>', UpdateBook.as_view(), name="update_book"),
    path('remove/<int:book_id>/', RemoveBook.as_view(), name='remove_book'),
    path('books/received-orders/', ReceivedOrdersView.as_view(), name='received_orders'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)