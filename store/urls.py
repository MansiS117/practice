from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from .views import BookDetailView , HomeView ,CategoryDetailView



urlpatterns = [
   
    path("" , HomeView.as_view(), name = "home"),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path("details/<int:pk>/" , BookDetailView.as_view() , name = "book_detail"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)