from django.shortcuts import render
from apps.store.models import Product,BrandCategory

# Create your views here.

def frontpage(request):
    featured_products = Product.objects.filter(is_featured=True)
    brands = BrandCategory.objects.all()


    context={'products':featured_products, 'brands_category':brands}

    return render(request,'core/frontpage1.html',context)
