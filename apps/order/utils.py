from apps.cart.cart import Cart

from apps.order.models import Order,OrderItem

def checkout(request,first_name, last_name, email, address):
    order = Order(first_name=first_name, last_name=last_name, email=email, address=address)

    cart = Cart(request)

    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'],quantity=item['quantity'])

    return order.id