from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView

from .forms import BookForm, ProfileForm, RegistrationForm
from .models import (
    Book,
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    Profile,
    User,
)
from django.conf import settings  # new
from django.urls import reverse  # new
import stripe

# Create your views here.


# views.py


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request):
        categories = Category.objects.all()
        books = Book.objects.order_by("created")
        user_type = (
            request.user.user_type if request.user.is_authenticated else None
        )
        context = {
            "categories": categories,
            "books": books,
            "user_type": user_type,
        }
        return render(request, self.template_name, context)


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()  # Retrieve the category instance
        context["books"] = Book.objects.filter(category=category)
        context["book_count"] = context["books"].count()
        if self.request.user.is_authenticated:
            context["user_type"] = self.request.user.user_type
        else:
            context["user_type"] = None

        return context


class BookDetailView(View):
    template_name = "book_detail.html"

    def get(self, request, book_id):
        # Retrieve the book object using the primary key (pk) from the URL
        book = get_object_or_404(Book, pk=book_id)
        user_type = (
            request.user.user_type if request.user.is_authenticated else None
        )

        # Define the context to be passed to the template
        context = {
            "book": book,
            "user_type": user_type,
        }

        # Render the template with the context
        return render(request, self.template_name, context)


## search
class SearchView(View):
    template_name = "category_detail.html"

    def get(self, request):
        keyword = request.GET.get("keyword", "")

        if keyword:
            books = Book.objects.order_by("-created").filter(
                Q(description__icontains=keyword)
                | Q(title__icontains=keyword)
                | Q(category__name__icontains=keyword)
                | Q(author__icontains=keyword)
            )
            book_count = books.count()
        else:
            books = Book.objects.none()  # Empty queryset
            book_count = 0

        context = {
            "books": books,
            "book_count": book_count,
            "keyword": keyword,
        }
        return render(request, self.template_name, context)


class RegistrationView(View):
    template_name = "register.html"

    def get(self, request):
        # if request.user.is_authenticated:
        #     return redirect("home")
        form = RegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        # if request.user.is_authenticated:
        #     return redirect("home")

        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set the user's password securely
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if password == confirm_password:
                user.set_password(password)
                user.save()

                messages.success(request, "Account Created Successfully!")
                return redirect("home")
            else:
                # Handle password mismatch error here
                messages.error(request, "Password does not match.")

        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "signin.html"

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_type == "seller":
                return redirect(
                    "dashboard"
                )  # Redirect sellers to the dashboard
            else:
                return redirect("home")  # Redirect buyers to the home page
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        user_password = request.POST.get("password")
        user = authenticate(
            request, username=email, password=user_password
        )  # Ensure email-based authentication

        if user is not None:
            login(request, user)
            # Check user type and redirect accordingly
            if user.user_type == "seller":
                messages.success(request, "Logged in successfully.")
                return redirect(
                    "dashboard"
                )  # Redirect sellers to the dashboard
            else:
                messages.success(request, "Logged in successfully.")
                return redirect("home")  # Redirect buyers to the home page
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect("login")  # Redirect to the login page on error


@login_required(login_url="login")
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect("login")


class CartView(View):
    template_name = "cart.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(
                "login"
            )  # Redirect to the login page if the user is not authenticated

        cart = Cart.objects.filter(buyer=request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)

            total_price = 0.0
            for item in cart_items:
                item.total_price = float(item.book.price) * float(
                    item.quantity
                )
                total_price += item.total_price

            context = {
                "cart": cart,
                "cart_items": cart_items,
                "total_price": total_price,
            }
        else:
            context = {
                "cart": None,
                "cart_items": [],
                "total_price": 0.0,
            }

        return render(request, self.template_name, context)


# Add the book into the cart
class AddToCartView(View):
    template_name = "cart.html"

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)

        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return redirect(
                "login"
            )  # Redirect to login if the user is not authenticated

        if book.stock <= 0:
            messages.error(request, "No more books available in stock.")
            return redirect(
                "cart"
            )  # Redirect to cart or show an error message

        # Get or create a cart for the current user
        if book:
            cart = Cart.objects.filter(buyer=request.user).first()
            if not cart:
                cart = Cart(buyer=request.user)
                cart.save()

            cart_item = CartItem.objects.filter(cart=cart, book=book).first()
            if not cart_item:
                if book.stock >= 1:  # Check if there is stock available
                    cart_item = CartItem(cart=cart, book=book, quantity=1)
                    cart_item.save()
                    book.stock -= 1  # Reduce stock by 1
                    book.save()  # Save the updated stock
            else:
                if book.stock >= (
                    cart_item.quantity + 1
                ):  # Ensure enough stock for an increase
                    cart_item.quantity += 1
                    cart_item.save()
                    book.stock -= 1  # Reduce stock by 1
                    book.save()  # Save the updated stock

        return redirect("cart")


class QuantityView(View):
    template_name = "cart.html"

    def post(self, request):
        cart_item_id = request.POST.get("cart_item_id")
        quantity_action = request.POST.get("quantity_action")

        cart_item = CartItem.objects.filter(id=cart_item_id).first()

        if cart_item:
            book = cart_item.book  # Get the related book

            if quantity_action == "increase":
                if book.stock > 0:  # Check if there's stock available
                    cart_item.quantity += 1
                    book.stock -= 1  # Decrease stock
                    cart_item.save()
                    book.save()  # Save the book instance to update stock
                else:
                    messages.error(
                        request, "No more books available in stock."
                    )
            elif quantity_action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    book.stock += 1  # Increase stock when decreasing

            cart_item.save()
            book.save()  # Save the book instance to update stock

        return redirect("cart")


# Remove the items from the cart
class RemoveView(View):
    template_name = "cart.html"

    def post(self, request, item_id):
        item = CartItem.objects.filter(id=item_id).first()

        if item:
            # Update the stock based on the quantity being removed
            book = item.book
            book.stock += (
                item.quantity
            )  # Add back the entire quantity of this item
            book.save()  # Save the book instance to update stock

            item.delete()  # Remove the item from the cart
            messages.success(request, "Item removed successfully")
        else:
            messages.error(request, "Item does not exist")

        return redirect("cart")


# dashboard
@login_required(login_url="login")
def dashboard(request):
    user_type = request.user.user_type

    if user_type == "seller":
        books = Book.objects.filter(seller=request.user)
        return render(
            request, "dashboard.html", {"user_type": user_type, "books": books}
        )

    elif user_type == "buyer":
        # Fetch buyer-specific data (e.g., orders)
        orders = Order.objects.filter(buyer=request.user).prefetch_related(
            "order_items"
        )
        return render(
            request,
            "dashboard.html",
            {"user_type": user_type, "orders": orders},
        )

    else:
        return render(request, "dashboard.html", {"user_type": "unknown"})


class ProfileView(View):
    template_name = "update_profile.html"

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect("home")

        # if request.user.user_type != "Buyer":
        #     return redirect("seller_profile")

        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            profile = Profile(user=request.user)
            profile.save()

        form = ProfileForm(instance=profile)
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()
        form = ProfileForm(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()

        return redirect("profile")


class OrderView(View):
    template_name = "place-order.html"

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(
                request, "You need to be logged in to place an order"
            )
            return redirect("login")

        cart = Cart.objects.filter(buyer=request.user).first()
        if not cart:
            messages.error(request, "No cart found for user")
            return redirect("cart")

        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            messages.error(request, "Your cart is empty")
            return redirect("cart")

        # Calculate total price, tax, and final total
        total_price = 0.0
        tax_rate = 0.10
        for item in cart_items:
            item.total_price = float(item.book.price) * float(item.quantity)
            total_price += item.total_price

        context = {
            "cart": cart,
            "cart_items": cart_items,
            "total_price": total_price,
        }

        # return self.render_to_response(context)
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(
                request, "You need to be logged in to place an order"
            )
            return redirect("login")

        cart = Cart.objects.filter(buyer=request.user).first()

        cart_items = CartItem.objects.filter(cart=cart)
        print("Cart items:", cart_items)
        total_price = 0.0
        line_items = []

        for item in cart_items:
            item.total_price = float(item.book.price) * float(item.quantity)
            total_price += item.total_price

            line_items.append(
                {
                    "price_data": {
                        "currency": "inr",
                        "product_data": {
                            "name": item.book.title,
                            # "images": [item.book.image.url] if item.book.image else [],  # Ensure this is a list of URLs
                        },
                        "unit_amount": int(
                            item.book.price * 100
                        ),  # Use the price in rupees directly
                    },
                    "quantity": item.quantity,
                }
            )

        # Create the order
        order = Order.objects.create(
            buyer=request.user,
            total_price=total_price,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                unit_price=item.book.price,
            )

        cart_items.delete()

        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create the checkout session with dynamic line items
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,  # Use the dynamically created line items
            mode="payment",
            success_url=request.build_absolute_uri(
                reverse("success", kwargs={"order_id": order.id})
            ),
        )

        return redirect(checkout_session.url, code=303)


class SuccessView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)  # Fetch the order by ID
        order_items = OrderItem.objects.filter(order=order)
        customer = order.buyer  # Get the order items

        context = {
            "order": order,
            "order_items": order_items,
            "customer": customer,
        }
        return render(
            request, "order_complete.html", context
        )  # Create this template


# add a new book for seller
class AddBook(View):
    template_name = "add_book.html"

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "You need to add a book")
            return redirect("login")

        form = BookForm()
        return render(request, "add_book.html", {"form": form})

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "You need to login")
            return redirect("login")
        user_type = request.user.user_type
        if request.user.user_type != "seller":
            messages.error(
                request, "You are not authorized to view this page."
            )
            return redirect("home")
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            messages.success(request, "book created successfully!")
            return redirect("dashboard")
        else:
            messages.error(request, "There was an error with your submission.")

        # If the form is not valid, re-render the form with error messages
        return self.render_to_response({"form": form})


# update book for seller
class UpdateBook(View):
    template_name = "add_book.html"

    def get(self, request, book_id):
        book = Book.objects.filter(id=book_id).first()
        if not book:
            messages.error(request, "book not found.")
            return redirect("dashboard")

        form = BookForm(instance=book)
        return render(
            request, self.template_name, {"form": form, "book": book}
        )

    def post(self, request, book_id):
        book = Book.objects.filter(id=book_id).first()
        if not book:
            messages.error(request, "book not found.")
            return redirect("dashboard")

        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "book updated successfully!")
            return redirect("dashboard")
        else:
            messages.error(request, "There was an error with your submission.")

        return render(
            request, self.template_name, {"form": form, "book": book}
        )


# remove book for seller
class RemoveBook(View):
    def get(self, request, book_id):
        # Get the book object, or return a 404 if it does not exist
        book = get_object_or_404(Book, id=book_id)

        # Optionally check if the user has permission to delete the book
        if request.user != book.seller:
            messages.error(
                request, "You are not authorized to delete this book."
            )
            return redirect("dashboard")

        # Delete the book
        book.delete()
        messages.success(request, "Book removed successfully!")
        return redirect("dashboard")


# recieved order for seller
class ReceivedOrdersView(View):
    template_name = "received_orders.html"

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to view orders.")
            return redirect("login")

        if request.user.user_type != "seller":
            messages.error(
                request, "You are not authorized to view this page."
            )
            return redirect("dashboard")

        # Retrieve orders for which the current seller's books are included
        seller_books = Book.objects.filter(seller=request.user)
        orders = Order.objects.filter(
            order_items__book__in=seller_books
        ).distinct()

        # Count orders for each book
        book_order_counts = {}
        for order in orders:
            for item in order.order_items.all():
                if item.book not in book_order_counts:
                    book_order_counts[item.book] = 0
                book_order_counts[item.book] += item.quantity

        context = {
            "orders": orders,
            "book_order_counts": book_order_counts,
        }

        return render(request, self.template_name, context)
