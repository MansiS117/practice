from celery import shared_task
from django.utils import timezone
from django.db.models import Sum
from .models import Order, DailySalesReport, User

@shared_task
def calculate_daily_sales():
    today = timezone.now().date()
    sellers = User.objects.filter(user_type='seller')  # Assuming you have a User model with user_type field

    for seller in sellers:
        # Calculate total sales for today for each seller
        total_sales = Order.objects.filter(ordered_at__date=today, seller=seller).aggregate(Sum('total_price'))['total_price__sum'] or 0.00
        
        # Update or create the daily sales report for the seller
        DailySalesReport.objects.update_or_create(
            date=today,
            seller=seller,  # Pass the seller instance directly
            defaults={'total_sales': total_sales}
        )
