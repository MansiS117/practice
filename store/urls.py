from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# from django.contrib.auth import views as auth_views

from . import views
from .views import (
    AddBook,
    AddToCartView,
    BookDetailView,
    CartView,
    CategoryDetailView,
    HomeView,
    LoginView,
    OrderView,
    ProfileView,
    QuantityView,
    ReceivedOrdersView,
    RegistrationView,
    RemoveBook,
    RemoveView,
    SearchView,
    UpdateBook,
    SuccessView,
    OrderSuccessView,
    DailySalesReportView,
    ResetPasswordView,
    ResetDoneView,
    ResetConfirmView,
    ResetCompleteView,
    CustomPasswordChangeView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "category/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "details/<int:book_id>/", BookDetailView.as_view(), name="book_detail"
    ),
    path("cart", CartView.as_view(), name="cart"),
    path(
        "addtocart/<int:book_id>/", AddToCartView.as_view(), name="add_to_cart"
    ),
    path("cart/quantity/", QuantityView.as_view(), name="quantity_item"),
    path(
        "cart/remove/<int:item_id>/", RemoveView.as_view(), name="remove_item"
    ),
    path("search", SearchView.as_view(), name="search"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("order/", OrderView.as_view(), name="order"),
    path("update_profile/", ProfileView.as_view(), name="profile"),
    path("add_book/", AddBook.as_view(), name="new_book"),
    path(
        "update_book/<int:book_id>", UpdateBook.as_view(), name="update_book"
    ),
    path("remove/<int:book_id>/", RemoveBook.as_view(), name="remove_book"),
    path(
        "books/received-orders/",
        ReceivedOrdersView.as_view(),
        name="received_orders",
    ),
    path(
        "daily-sales-report/",
        DailySalesReportView.as_view(),
        name="daily_sales_report",
    ),
    path("order/success/", OrderSuccessView.as_view(), name="order_success"),
    path("success/<int:order_id>/", SuccessView.as_view(), name="success"),
    path("password_reset/", ResetPasswordView.as_view(), name="reset"),
    path(
        "password_reset/done/",
        ResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        ResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        ResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "change-password/",
        CustomPasswordChangeView.as_view(),
        name="change_password",
    ),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
