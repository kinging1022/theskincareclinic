import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Location,  DeliveryPrice , Area
from apps.cart.cart import Cart


def api_get_area(request):
    location_name = request.GET.get('location', '')

    try:
        location = Location.objects.get(location=location_name)
    except Location.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Location not found'})

    areas = [
        {'id': area.id, 'title': area.area} for area in location.areas.all()
    ]

    print(areas)
    return JsonResponse({'success': True, 'areas': areas})



def api_get_delivery_price(request):
    area_name = request.GET.get('area', '')
    

    if not area_name:
        return JsonResponse({'success': False, 'error': 'Missing area parameter'})

    try:
        area = Area.objects.get(area=area_name) 
    except Area.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Area not found'})

    cart = Cart(request)
    total_weight = sum(item['product'].weight * int(item['quantity']) for item in cart)

    delivery_price = DeliveryPrice.objects.filter(
        location=area,
        weight_from__lte=total_weight,
        weight_to__gte=total_weight
    ).first()

    

    if delivery_price:
        return JsonResponse({
            'success': True,
            'delivery_price': delivery_price.price,
            'area_name': area.area  # Use area.area for the name
        })
    else:
        return JsonResponse({'success': False, 'error': 'Delivery price not found'})
