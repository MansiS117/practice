from django.shortcuts import render , get_object_or_404 , redirect
from django.views import View
from django.views.generic.detail import DetailView 
from django.views.generic import TemplateView , ListView 
from .models import Book , Category , User , Cart , CartItem
from django.db.models import Q
from . forms import RegistrationForm 
from django.contrib.auth import login , authenticate , logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.


# views.py

class HomeView(TemplateView):
    template_name = 'home.html'
  
    def get(self , request):
        categories = Category.objects.all()
        books = Book.objects.order_by("created")
        context = {"categories" : categories , "books" : books}
        return render(request , self.template_name , context)


class CategoryDetailView(DetailView) :
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get(self , request , pk ):
        category = get_object_or_404(Category,pk = pk)
        books = Book.objects.filter(category = category)
        book_count = books.count()
        context = {"category" : category , "books" : books ,  "book_count" : book_count }
        return render(request , self.template_name , context)
 
# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'book_detail.html'
#     context_object_name = 'book'

class BookDetailView(View):
    template_name = 'book_detail.html'
    
    def get(self, request, book_id):
        # Retrieve the book object using the primary key (pk) from the URL
        book = get_object_or_404(Book, pk = book_id)
        
        # Define the context to be passed to the template
        context = {
            'book': book
        }
        
        # Render the template with the context
        return render(request, self.template_name, context)


## search
def search(request):
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            books = Book.objects.order_by('-created').filter(Q(description__icontains = keyword) | Q(title__icontains = keyword) | Q(category__name__icontains = keyword) | Q(author__icontains = keyword))
            book_count = books.count()
           
        else:
            books = Book.objects.none()  # Empty queryset
            book_count = 0

    context = {
                "books" : books,
                "book_count" : book_count,
                "keyword" : keyword,
            }
    return render(request , 'category_detail.html' , context)


class RegistrationView(TemplateView):
    template_name = "register.html"

    def get(self, request):
        # if request.user.is_authenticated:
        #     return redirect("/")
        form = RegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        # if request.user.is_authenticated:
        #     return redirect("/")

        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # send_verification_email(user, request)
            messages.success(request, "Account Created Successfully!")
            return redirect("/")

        return render(request, self.template_name, {"form": form})
    

class LoginView(TemplateView):
    template_name = "signin.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        user_password = request.POST.get("password")
        user = authenticate(request, username=email, password=user_password)  # Ensure email-based authentication

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("/")  # Redirect to the homepage or another page after login
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect("login")  # Redirect to the login page on error


@login_required(login_url = "login")
def user_logout(request):
    logout(request)
    messages.success(request , "You are logged out")
    return redirect("login")


class CartView(TemplateView):
    template_name = "cart.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to the login page if the user is not authenticated

        cart = Cart.objects.filter(buyer=request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)

            total_price = 0.0
            for item in cart_items:
                item.total_price = float(item.book.price) * float(item.quantity)
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


# Add the product into the cart


class AddToCartView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)

        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if the user is not authenticated

        # Get or create a cart for the current user
        if book:
            cart = Cart.objects.filter(buyer=request.user).first()
            if not cart:
                cart = Cart(buyer=request.user)
                cart.save()

            cart_item = CartItem.objects.filter(
                cart=cart, book=book
            ).first()
            if not cart_item:
                cart_item = CartItem(cart=cart, book=book, quantity=1)
                cart_item.save()
            else:
                cart_item.quantity += 1
                cart_item.save()

        return redirect('cart')

class QuantityView(TemplateView):
    template_name = "cart.html"
    def post(self, request):
        cart_item_id = request.POST.get("cart_item_id")
        quantity_action = request.POST.get("quantity_action")

        cart_item = CartItem.objects.filter(id=cart_item_id).first()

        if cart_item:
            if quantity_action == "increase":
                cart_item.quantity += 1
            elif quantity_action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1

            cart_item.save()

        return redirect("cart")


# Remove the items from the cart


class RemoveView(TemplateView):
    template_name = "cart.html"
    def post(self, request, item_id):
        item = CartItem.objects.filter(id=item_id).first()

        if item:
            item.delete()
            messages.success(request, "item removed successfully")
        else:
            messages.error(request, "item does not exist")

        return redirect("cart")