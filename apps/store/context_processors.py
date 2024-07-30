from .models import Category, BrandCategory



def menu_categories(request):
    categories = Category.objects.filter(parent=None)


    return {'menu_categories': categories}


def brand_categories(request):
    categories = BrandCategory.objects.all()


    return  {'brand_categories':categories}