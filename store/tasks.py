from celery import shared_task
from django.utils import timezone
from django.db.models import Sum
from .models import OrderItem, DailySalesReport, User


@shared_task
def calculate_daily_sales():
    today = timezone.now().date()
    sellers = User.objects.filter(user_type="seller")  # Get all sellers

    for seller in sellers:
        # Calculate total sales for today for each seller using related_name 'order_items'
        total_sales = (
            OrderItem.objects.filter(
                order__ordered_at__date=today,  # Filter by the order date
                seller=seller,  # Filter by the seller in the OrderItem
            ).aggregate(total_sales=Sum("unit_price"))["total_sales"]
            or 0.00
        )

        # Update or create the daily sales report for the seller
        DailySalesReport.objects.update_or_create(
            date=today, seller=seller, defaults={"total_sales": total_sales}
        )
