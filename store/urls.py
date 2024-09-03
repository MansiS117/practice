from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import BookDetailView, HomeView ,CategoryDetailView



urlpatterns = [
   
    path("" ,HomeView.as_view(), name = "home"),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path("details/<int:pk>/" , BookDetailView.as_view() , name = "book_detail"),
    path('cart' , views.cart , name = 'cart'),
    path('search' , views.search , name = 'search'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)