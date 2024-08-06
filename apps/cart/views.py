from django.shortcuts import render
from .cart import Cart

# Create your views here.

def cart(request):
    cart = Cart(request)
    products_list = []

    for item in cart:
        product = item['product']
        
        
        url = f"/{product.category.slug}/{product.slug}/"
        print(f"Constructed URL: {url}") 

        product_details = {
            'id': product.id,
            'title': product.title,
            'price': product.price,
            'quantity': item['quantity'],
            'total_price': item['total_price'],
            'thumbnail': product.get_thumbnail(), 
            'url': url,
            'num_available': product.num_available,
        }
        
                 
        
        

        products_list.append(product_details) 


    context = {'cart':cart, 'products_list':products_list}
    return render(request,'cart/cart.html',context)



def success(request):
    cart = Cart(request)
    cart.clear()

    return render(request,'cart/success.html')