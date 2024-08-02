import json
import requests
from django.shortcuts import get_object_or_404, redirect , render
from django.http import JsonResponse

from django.conf import settings
from apps.cart.cart import Cart

from .models import Product
from apps.order.utils import checkout 
from apps.coupon.models import Coupon


def api_create_checkout_session(request):
        if request.method == 'POST':    

            cart = Cart(request)
            
            data = json.loads(request.body)
            
            coupon_code = data['coupon_code']
            coupon_value = 0

            if coupon_code != '':
                coupon = Coupon.objects.get(code=coupon_code)

                if coupon.can_use:
                    coupon_value = coupon.value
                    coupon.use()

            order_id = checkout(request, data['first_name'],data['last_name'],data['email'],data['address'],data['phone'])
            
            
            amount = cart.get_total_cost()
            if coupon_value > 0:
                amount = cart.get_total_cost() - coupon_value
            
            
            try:                

                # Paystack API endpoint
                url = "https://api.paystack.co/transaction/initialize"

                # Metadata for checkout session
                metadata = json.dumps({
                    "order_id" : order_id,
                    "cancel_action": 'http://127.0.0.1:8000/cart/'  
                })

                # Paystack checkout session data

                session_data = {
                    'email': data['email'],
                    'amount': amount * 100,
                    'callback_url': 'http://127.0.0.1:8000/cart/success/',  # success url
                    'metadata': metadata
                }

                # Set up headers with Paystack secret key
                headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}

                # Make API request to Paystack
                response = requests.post(url, headers=headers, json=session_data)
                response_data = response.json()
                #print(response_data)

                if response.status_code == 200 and response_data["status"] == True:
                    redirect_url = response_data["data"]["authorization_url"]
                    return JsonResponse({'redirect_url': redirect_url})
                else:
                    # Handle errors (e.g., log error, return error message)
                    #print(f"Error: {response_data['message']}")
                    return JsonResponse({'error': 'An error occurred during checkout.'}, status=400)

            except Exception as e:
                # Handle unexpected errors (e.g., log error, return generic error message)
                #print(f"Unexpected error: {e}")
                return JsonResponse({'error': 'An error occurred during checkout.'}, status=500)

        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)










def api_add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    

    cart = Cart(request)

    product = get_object_or_404(Product,pk=product_id)

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)
        
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)
        

    return JsonResponse ({'success':True})



def api_remove_from_cart(request):
    data = json.loads(request.body)
    product_id = str(data['product_id'])


    cart = Cart(request)
    cart.remove(product_id)

    return JsonResponse({'success':True})