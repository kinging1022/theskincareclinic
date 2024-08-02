from django.shortcuts import render
from .cart import Cart

# Create your views here.

def cart(request):
    cart = Cart(request)
    productstring = ''

    for item in cart:
        product = item['product']
        url = '/%s/%s' % (product.category.slug, product.slug)
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'url': '%s', 'num_available': '%s'}," % (product.id, product.title, product.price, item['quantity'], item['total_price'], product.get_thumbnail(), url, product.num_available)

        productstring = productstring + b


    context = {'cart':cart, 'productstring':productstring}
    return render(request,'cart/cart.html',context)



def success(request):
    cart = Cart(request)
    cart.clear()

    return render(request,'cart/success.html')