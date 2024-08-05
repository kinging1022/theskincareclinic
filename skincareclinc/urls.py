"""
URL configuration for skincareclinc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.views import frontpage
from apps.store.views import category_details, product_details, brand_details
from apps.store.api import api_add_to_cart , api_remove_from_cart , api_create_checkout_session
from apps.coupon.api import api_can_use
from apps.cart.views import cart , success
from apps.cart.webhook import paystack_webhook
from apps.order.views import admin_order_pdf

from .sitemap  import StaticViewSitemap, CategorySitemap, ProductSitemap

sitemaps = {'static': StaticViewSitemap, 'product':ProductSitemap, 'category': CategorySitemap }



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),
    path('api/remove_from_cart/',api_remove_from_cart, name='api_remove_from_cart'),
    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/create_checkout_session/',api_create_checkout_session,name='api_create_checkout_session'),
    path('api/can_use/',api_can_use, name='api_can_use'),
    path('admin_order_pdf/<int:order_id>/',admin_order_pdf, name="admin_order_pdf"),
    path('cart/', cart, name='cart'),
    path('hooks/',paystack_webhook, name='paystack_webhook'),
    path('cart/success/', success, name='success'),
    path('brand/<slug:brand_slug>/', brand_details, name='brand_details'), 
    path('<slug:category_slug>/<slug:slug>/', product_details, name='product_details'),
    path('<slug:slug>/', category_details, name='category_details'),
    path("sitemap.xml", sitemap, {"sitemaps":sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    
    
    #api
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

