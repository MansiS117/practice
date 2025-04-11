def calculate_cart_totals(cart_items):
    total_price = 0.0
    line_items = []

    for item in cart_items:
        item_total_price = float(item.book.price) * float(item.quantity)
        total_price += item_total_price

        line_items.append(
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": item.book.title,
                    },
                    "unit_amount": int(item.book.price * 100),
                },
                "quantity": item.quantity,
            }
        )

    return total_price, line_items
