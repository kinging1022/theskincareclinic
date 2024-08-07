from django.shortcuts import render , get_object_or_404
from .models import Category ,BrandCategory,Product
from apps.cart.cart import Cart
# Create your views here.

from django.db.models import Q
from datetime import datetime
import random

def search(request):
    query = request.GET.get('query','')
    instock = request.GET.get('instock','')
    try:
        price_from = int(request.GET.get('price_from',0))
    except ValueError:
        price_from = 0

    try:
        price_to = int(request.GET.get('price_to', 20000))
    except ValueError:
        price_to = 20000
    
    sorting = request.GET.get('sorting', '-date_added')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(price__gte=price_from).filter(price__lte=price_to)


    if instock:
        products = products.filter(num_available__gte=1)

    context = {
    'query': query,
    'products': products.order_by(sorting),
    'instock':instock,
    'price_from':price_from,
    'price_to':price_to,
    'sorting':sorting,
    }
        
    return render(request, 'store/search.html', context)

    




def category_details(request,slug):
    category = get_object_or_404(Category,slug=slug)
    products = category.products.filter(parent=None)



    return render(request, 'store/category_details.html',{'category':category, 'products':products})


def product_details(request,category_slug,slug):
    product = get_object_or_404(Product,slug=slug)
    similar_products = product.category.products.all()
    product.num_visits = product.num_visits + 1
    product.last_visits = datetime.now()
    product.save()

    imagelist = []
    
    for image in product.images.all():
        more_images = {'thumbnail': image.thumbnail.url, 'image': image.image.url}

        imagelist.append(more_images)
    
    
    cart = Cart(request)

    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False
    
    
    context = {
        'product':product,
        'imagelist':imagelist,
        'similar_products':similar_products,
    }


    return render(request,'store/product_details.html',context)



def brand_details(request, brand_slug):
    brand = get_object_or_404(BrandCategory, slug=brand_slug)
    products = Product.objects.filter(brand=brand)
    context = {
        'brand': brand,
        'products': products,
    }
    return render(request, 'store/brand_details.html', context)



