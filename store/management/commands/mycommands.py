from django.core.management.base import BaseCommand
from store.models import Book , Category

class Command(BaseCommand):
     help = 'Initialize the database with default categories and sample books'

     def handle(self, *args, **kwargs):
           # Create default categories
        categories = ['Fiction', 'Non-Fiction', 'Science', 'History']
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
            
        self.stdout.write(self.style.SUCCESS('Database successfully initialized with default data'))
