from django.contrib import admin

from .models import DeliveryPrice, Location, Area

# Register your models here.

admin.site.register(DeliveryPrice)
admin.site.register(Location)
admin.site.register(Area)

