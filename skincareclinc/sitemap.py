from django.contrib.sitemaps import Sitemap
from django.db.models.base import Model
from django.shortcuts import resolve_url

from apps.store.models import Category, Product


class StaticViewSitemap(Sitemap):
    def items(self):
        return['frontpage']
    

    def location(self, item):
        return resolve_url(item)
    

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5


    def items(self):
        return Category.objects.all()
    

    def location(self,category):
        return category.get_absolute_url()
    


class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7


    def items(self):
        return Product.objects.all()
    

    def location(self,product):
        return product.get_absolute_url()
    

    def lastmod(self,obj):
        return obj.date_added
    