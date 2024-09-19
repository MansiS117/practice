from django.urls import path

from api import views

from .views import LoginView, RegistrationView

urlpatterns = [
    path("books/", views.book_list, name="books"),
    path("register/", RegistrationView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="api-login"),
]
