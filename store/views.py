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
 

# def book_detail(request , pk):
#     book = get_object_or_404(Book , pk=pk)
#     context = {
#         "book"  : book 
#     }
#     return render(request , "book_detail.html" , context) 

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

## cart

def cart(request):
    cart_items = CartItem.objects.filter(buyer=request.user)
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
    # return render(request , "cart.html")


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



    
 
# def add_to_cart(request, product_id):
#     book = Book.objects.get(id=product_id)
#     cart_item, created = CartItem.objects.get_or_create(book=book, user=request.user)
#     cart_item.quantity += 1
#     cart_item.save()
#     return redirect('cart:view_cart')
 
# def remove_from_cart(request, item_id):
#     cart_item = CartItem.objects.get(id=item_id)
#     cart_item.delete()
#     return redirect('cart:view_cart')