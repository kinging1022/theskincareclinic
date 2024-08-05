import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe

from django.urls import reverse
from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem

def order_name(obj):
    return f"{obj.first_name} {obj.last_name}"

order_name.short_description = 'Name'


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('admin_order_pdf', args=[obj.id])))

order_pdf.short_description = 'PDF'

def admin_order_shipped(modeladmin, request, queryset):
    for order in queryset:
        order.shipped_date = timezone.now()
        order.status = Order.SHIPPED
        order.save()

        html_content = render_to_string('core/order_sent.html',{'order':order})
        from_email = settings.DEFAULT_FROM_EMAIL
        subject = 'shop order sent'
        text_content = 'Order sent, Your order has been sent sucessfully'
        msg = EmailMultiAlternatives(subject,text_content, from_email, [order.email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    return 
admin_order_shipped.short_description = 'Set shipped'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', order_name, 'transaction_ref'  , 'status', 'created_at', order_pdf]
    list_filter = ['created_at', 'status']
    search_fields = ['first_name', 'address']
    inlines= [OrderItemInline]
    actions=[admin_order_shipped]

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)