import json
from datetime       import datetime

from django.http    import JsonResponse
from django.views   import View

from user.utils     import login_decorator
from user.models    import Address
from product.models import ProductStock 
from .models        import (
    Order,
)

class CartView(View):
     @login_decorator
     def get(self, request):
        user = request.user
        
        if not Order.objects.filter(user=user, order_status_id=1).exists():
            return JsonResponse({"message": "EMPTY"}, status=200)
        
        order_exist          = Order.objects.get(user=user, order_status_id=1)
        order_products_exist = order_exist.orderproductstock_set.filter(order=order_exist)
        
        cart_product_list = []
        for order_product_exist in order_products_exist:
            product_SSP  = order_product_exist.product_stock 
            product      = product_SSP.product
            product_info = {
                "category"        : product.category.menu.name,
                "productId"       : product.id,
                "productName"     : product.name,
                "productSubName"  : product.sub_name,
                "productStockId"  : product_SSP.id,
                "productSize"     : product_SSP.size,
                "productPrice"    : product_SSP.price,
                "productStock"    : product_SSP.stock,
                "productImageUrl" : product.image_set.get(is_main=True).image_url,
                "productQuantity" : order_product_exist.quantity
            }
            cart_product_list.append(product_info)

        data = {
            "orderNumber": order_exist.order_number,
            "carts": cart_product_list,
        }

        return JsonResponse({"data": data, "message": "SUCCESS"}, status=200)

