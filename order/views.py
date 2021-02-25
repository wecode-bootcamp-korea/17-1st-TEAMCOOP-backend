import json
from datetime               import datetime

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from user.utils             import login_decorator
from user.models            import Address
from product.models         import ProductStock 
from .models                import Order, OrderProductStock, OrderStatus

class CartView(View):
    @login_decorator
    def get(self, request):
        try:
            user = request.user
            
            if not Order.objects.filter(user=user, order_status=OrderStatus.objects.get(name='주문 전')).exists():
                return JsonResponse({"message": "EMPTY"}, status=200)
            
            order          = Order.objects.get(user=user, order_status=OrderStatus.objects.get(name='주문 전'))
            order_products = order.orderproductstock_set.filter(order=order)
        
            cart_product_list = [{
                "category"        : order_product.product_stock.product.category.menu.name,
                "productId"       : order_product.product_stock.product.id,
                "productName"     : order_product.product_stock.product.name,
                "productSubName"  : order_product.product_stock.product.sub_name,
                "productStockId"  : order_product.product_stock.id,
                "productSize"     : order_product.product_stock.size,
                "productPrice"    : order_product.product_stock.price,
                "productStock"    : order_product.product_stock.stock,
                "productImageUrl" : order_product.product_stock.product.image_set.get(is_main=True).image_url,
                "productQuantity" : order_product.quantity
                } for order_product in order_products
            ]

            data = {
                "orderNumber": order.order_number,
                "carts": cart_product_list,
            }

            return JsonResponse({"data": data, "message": "SUCCESS"}, status=200)

        except OrderStatus.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)

    @login_decorator
    def post(self, request):
        try:
            data          = json.loads(request.body)
            user          = request.user
            product_id    = data['productId']
            product_size  = data.get('productSize', None)
            product_price = data['productPrice']

            product_price = float(product_price)

            if not Order.objects.filter(user=user, order_status=OrderStatus.objects.get(name='주문 전')).exists():
                shipping_cost = 5 if product_price < 20 else 0
                
                order_info    = Order.objects.create( 
                    user            = user,
                    order_number    = datetime.today().strftime("%Y%m%d") + str(randint(10000, 100000)),
                    order_status    = OrderStatus.objects.get(name='주문 전'),
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

            # order_product_stocks insert
            added_product = ProductStock.objects.get(product_id=product_id, size=product_size)
            OrderProductStock.objects.update_or_create(
                order         = order_info,
                product_stock = added_product,
                defaults      = {
                    "quantity" : 1
                }
            )

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except OrderStatus.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)
        
        except ProductStock.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)


    @login_decorator
    def patch(self, request):
        try:
            data             = json.loads(request.body)
            user             = request.user
            product_id       = data['productId']
            product_stock_id = data['productStockId']
            quantity_new     = data['productQuantity']
            size_new         = data.get('productSize', None)
            
            order = Order.objects.get(user=user, order_status=OrderStatus.objects.get(name='주문 전'))
            
            target_order_product      = OrderProductStock.objects.get(order=order, product_stock_id=product_stock_id) 
            target_order_product_size = target_order_product.product_stock.size
            product_new               = ProductStock.objects.get(product_id=product_id, size=size_new)

            # 변경할 상품이 이미 장바구니에 존재하는 경우
            if target_order_product_size != size_new:
                if OrderProductStock.objects.filter(order=order, product_stock=product_new).exists(): 
                    order_product_already_exist = OrderProductStock.objects.get(order=order, product_stock=product_new)

                    if bool(product_new.stock - quantity_new < 0):
                        return JsonResponse({"message": "OUT_OF_STOCK"}, status=200)

                    order_product_already_exist.quantity = quantity_new
                    order_product_already_exist.save()

                    # 원래 있던 상품은 새로 바꿀 상품이 이미 존재하는게 있으므로 삭제 
                    target_order_product.delete()
                    return JsonResponse({"message": "SUCCESS"}, status=200)

            # 변경할 상품이 장바구니에 없는 경우
            if bool(product_new.stock - int(quantity_new) < 0):
                return JsonResponse({"message": "OUT_OF_STOCK"}, status=200)

            target_order_product.product_stock = product_new
            target_order_product.quantity      = quantity_new
            target_order_product.save()

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except Order.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)

        except ProductStock.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)

        except OrderStatus.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)

        except MultipleObjectsReturned:
            return JsonResponse({"message": "MULTIPLE_OBJECTS_RETURNED"}, status=400)

class CartDetailView(View):
    @login_decorator
    def delete(self, request, product_stock_id):
        try:
            if not ProductStock.objects.filter(id=product_stock_id):
                return JsonResponse({"message": "DOES_NOT_EXIST"}, status=404)

            user          = request.user
            order         = Order.objects.get(user=user, order_status=OrderStatus.objects.get(name='주문 전'))
            order_product = order.product_stock.get(id=product_stock_id)

            order_product.delete()

            # 장바구니에 상품이 없을 경우 order 정보 삭제
            if not OrderProductStock.objects.filter(order=order).exists():
                order.delete()

            return JsonResponse({"message": "SUCCESS"}, status=200) 

        except Order.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)

        except MultipleObjectsReturned:
            return JsonResponse({"message": "MULTIPLE_OBJECTS_RETURNED"}, status=400)

        except OrderStatus.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)

        except OrderProductStock.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)

class CheckOutView(View):
    @login_decorator
    def get(self, request, order_number):
        user = request.user

        if not Order.objects.filter(order_number=order_number).exists():
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=404)

        order_info     = Order.objects.get(order_number=order_number)
        order_products = order_info.orderproductstock_set.all()

        cart_product_list = [{
            "category"        : order_product.product_stock.product.category.menu.name,
            "productId"       : order_product.product_stock.product.id,
            "productName"     : order_product.product_stock.product.name,
            "productSubName"  : order_product.product_stock.product.sub_name,
            "productStockId"  : order_product.product_stock.id,
            "productSize"     : order_product.product_stock.size,
            "productPrice"    : order_product.product_stock.price,
            "productIsSoldOut": bool(order_product.product_stock.stock - order_product.quantity <= 0),
            "productImageUrl" : order_product.product_stock.product.image_set.get(is_main=True).image_url,
            "productQuantity" : order_product.quantity
            } for order_product in order_products
        ]
         
        address_info = user.address_set.filter(is_main=True)
        address      = address_info[0].address if address_info else ""
        zip_code     = address_info[0].zip_code if address_info else ""
        user_info = {
            "userName"    : user.name,
            "email"       : user.email,
            "phoneNumber" : user.phone_number,
            "address"     : address,
            "zipcode"     : zip_code
        }

        data = {
            "orderNumber": order_info.order_number,
            "carts"      : cart_product_list,
            "user"       : user_info
        }

        return JsonResponse({"data": data, "message": "SUCCESS"}, status=200)
        
    @login_decorator
    def post(self, request, order_number):
        try:
            data = json.loads(request.body)
            sub_total_cost = data['subTotalCost']
            shipping_cost  = data['shippingCost']
            total_cost     = data['totalCost']
            address_order  = data['address']
            zipcode_order  = data['zipcode']
            user           = request.user

            order_info = Order.objects.get(order_number=order_number)
            order_info.order_status     = OrderStatus.objects.get(name='결제 완료')
            order_info.sub_total_cost   = float(sub_total_cost)
            order_info.shipping_cost    = float(shipping_cost)
            order_info.total_cost       = float(total_cost)
            order_info.save()

            Address.objects.update_or_create(
                user     = user,
                address  = address_order,
                zip_code = zipcode_order,
                order    = order_info,
                defaults = {
                    'is_main': False
                }
            )

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
