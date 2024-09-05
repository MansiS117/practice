from django.shortcuts import render , get_object_or_404
from django.views.generic.detail import DetailView 
from django.views.generic import TemplateView , ListView 
from .models import Book , Category 
from django.db.models import Q
# Create your views here.
# def home(request):
#     books = Book.objects.all()  
#     categories = Category.objects.all()
#     context = {
#         "books" : books ,
#         "categories" : categories
        
#      }
#     return render(request , "home.html", context)

# views.py

class HomeView(TemplateView):
    template_name = 'home.html'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
        
    #     # Add books and categories to the context
    #     context['books'] = Book.objects.all()
    #     context['categories'] = Category.objects.all()
        
    #     return context
    
    def get(self , request):
        categories = Category.objects.all()
        books = Book.objects.order_by("created")
        context = {"categories" : categories , "books" : books}
        return render(request , self.template_name , context)

# class HomeView(ListView):
#     model = Book  # Specify the model for the primary list view
#     template_name = 'home.html'
    
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get the context
#         context = super().get_context_data(**kwargs)
        
#         # Add categories to the context
#         context['categories'] = Category.objects.all()
        
#         return context
    
# def category_detail(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     books = Book.objects.filter(category=category)
#     return render(request, 'category_detail.html', {'category': category, 'books': books})
class CategoryDetailView(DetailView) :
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['books'] = Book.objects.filter(category=self.object)
    #     return context

    def get(self , request , pk ):
        category = get_object_or_404(Category , pk = pk)
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
    return render(request , "cart.html")

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