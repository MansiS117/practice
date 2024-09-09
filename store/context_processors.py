# myapp/context_processors.py
from .models import Cart, CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(buyer=request.user).first()
        if cart:
            count = CartItem.objects.filter(cart=cart).count()
        else:
            count = 0
    else:
        count = 0
    return {'cart_item_count': count}
