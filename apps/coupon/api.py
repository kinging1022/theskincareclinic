from django.http import JsonResponse

from .models import Coupon


def api_can_use(request):
    coupon_code = request.GET.get('coupon_code', '')

    try:
        coupon = Coupon.objects.get(code=coupon_code)

        if coupon.can_use():
            return JsonResponse({'amount':coupon.value})
        else:
            return JsonResponse({'amount':0})
        
    except Exception:
        return JsonResponse({'amount':0})
