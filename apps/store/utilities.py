from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from apps.order.views import render_to_pdf
from django.conf import settings
import logging

logger = logging.getLogger(__name__)





def decrement_product_quantity(order):
    for item in order.items.all():
        product = item.product
        product.num_available = product.num_available - item.quantity
        product.save()



def send_order_confirmation(order):
    html_content = render_to_string('core/order_confirmation.html',{'order':order})
    pdf = render_to_pdf('order/order_pdf.html', {'order':order})
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [order.email]
    subject = "The skincare clinic order confirmation"
    text_content = 'Your order is successful. Order confirmation details are attached in the email.'

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')


    if pdf:
        name = 'order_%s.pdf' % order.id
        msg.attach(name,pdf,'application/pdf')


    try:
        msg.send()
        logger.info("Order confirmation email sent successfully")
    except Exception as e:
        logger.error(f"Failed to send order confirmation email: {e}")
        # Handle the exception (e.g., retry, alert, etc.)