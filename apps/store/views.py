from django.shortcuts import render , get_object_or_404
from .models import Category ,BrandCategory,Product
from apps.cart.cart import Cart
# Create your views here.

def category_details(request,slug):
    category = get_object_or_404(Category,slug=slug)
    products = category.products.filter(parent=None)



    return render(request, 'store/category_details.html',{'category':category, 'products':products})


def product_details(request,category_slug,slug):
    product = get_object_or_404(Product,slug=slug)
    similar_products = product.category.products.all()

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



