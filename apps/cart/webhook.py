import json
import hashlib
import hmac
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from apps.order.models import Order
from apps.store.utilities import decrement_product_quantity, send_order_confirmation

def verify_signature(request_data, signature):
    secret_key = settings.PAYSTACK_SECRET_KEY
    hash = hmac.new(secret_key.encode('utf-8'), request_data, hashlib.sha512).hexdigest()
    return hash == signature

@csrf_exempt
def paystack_webhook(request):
    # Only process POST requests
    if request.method != 'POST':
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

    request_data = request.body
    signature = request.headers.get('X-Paystack-Signature')

    if not verify_signature(request_data, signature):
        return JsonResponse({'status': 'failed', 'message': 'Invalid signature'}, status=400)

    try:
        event = json.loads(request_data)
        metadata = event['data']['metadata']
        order_id = metadata.get('order_id', '')
        coupon_used = metadata.get('coupon_code','')
        paid_delivery = metadata.get('delivery_price', '0')

        try:
            order = Order.objects.get(pk=order_id)
            if event['event'] == 'charge.success':
                amount = float(event['data']['amount'])/100
                try:
                    delivery_amount = float(paid_delivery)
                except ValueError:
                    delivery_amount = 0.0
                
                order.paid = True
                order.paid_amount = amount - delivery_amount
                order.delivery_amount = delivery_amount
                order.transaction_ref = event['data']['reference']
                order.used_coupon = coupon_used
                order.save()

                decrement_product_quantity(order)
                send_order_confirmation(order)
            else:
                order.paid = False
                order.save()

            # Return a success response after processing the event
            return JsonResponse({'status': 'success', 'message': 'Order updated successfully'}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Order not found'}, status=404)
    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({'status': 'failed', 'message': 'Invalid event data'}, status=400)
