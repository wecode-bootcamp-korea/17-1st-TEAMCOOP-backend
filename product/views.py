import json
from datetime     import datetime
from random       import randint

from django.views import View
from django.http  import JsonResponse

from user.utils   import login_decorator
from order.models import Order, OrderProductStock
from .models      import (
    ProductStock,
)

class ProductToCartView(View):  
    @login_decorator
    def post(self, request):
            data          = json.loads(request.body)
            user          = request.user
            product_id    = data.get('productId', None)
            product_size  = data.get('productSize', None)
            product_price = data.get('productPrice', None)

            if not (product_id and product_price): 
                return JsonResponse({"message": "KEY_ERROR"}, status=400)            

            if not ProductStock.objects.filter(product_id=product_id, size=product_size):
                return JsonResponse({"message": "PRODUCT_DOES_NOT_EXIST"}, status=400)

            product_price = float(product_price)

            if not Order.objects.filter(user=user, order_status_id=1).exists():
                shipping_cost = 5 if product_price < 20 else 0
                
                order_info    = Order.objects.create( 
                    user            = user,
                    order_number    = datetime.today().strftime("%Y%m%d") + str(randint(10000, 100000)),
                    order_status_id = 1,
                    sub_total_cost  = product_price,
                    shipping_cost   = shipping_cost,
                    total_cost      = product_price + shipping_cost
                )
            else:
                order_info = Order.objects.get(user=user, order_status_id=1)
                order_info.sub_total_cost = float(order_info.sub_total_cost) + product_price
                order_info.shipping_cost  = 5 if order_info.sub_total_cost < 20 else 0
                order_info.total_cost     = float(order_info.sub_total_cost) + order_info.shipping_cost
                order_info.save()

            added_product = ProductStock.objects.get(product_id=product_id, size=product_size)
            OrderProductStock.objects.update_or_create(
                order         = order_info,
                product_stock = added_product,
                defaults      = {
                    "quantity" : 1
                }
            )

            return JsonResponse({"message": "SUCCESS"}, status=200)


