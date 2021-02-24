import json
from datetime import datetime
from random   import randint

from django.http  import JsonResponse, HttpResponse
from django.views import View

from user.utils     import login_decorator
from product.models import (Menu,
                            Category, 
                            Product,
                            Image,
                            ProductStock,
                            RelatedProduct,
                            Disease,
                            ProductDisease,
                            Allergy,
                            ProductAllergy,
                            Goal,
                            ProductGoal,
                            ProductDietaryHabit,
                            DietaryHabit,
                            VeganLevel,
                            ActivityLevel,
                            GenderCode,
                            AgeLevel)
from user.models    import User, Address
from order.models   import Promotion, Order, Review, OrderProductStock, OrderStatus, ShipmentStatus

class ProductView(View):
    def get(self, request, id=None):
        result            = []
        context           = {}
        product_info_list = []
        product_info      = {}

        sort     = request.GET.get('sort', all)
        sort_dic = {}
        sort_dic["lettervitamins"] = "Letter Vitamin"
        sort_dic["minerals"]       = "Minerals"
        sort_dic["herbs"]          = "Herbs"
        sort_dic["probiotics"]     = "Probiotics"
        sort_dic["collagens"]      = "Collagens"
        sort_dic["proteins"]       = "Proteins"
        sort_dic["boosts"]         = "Boosts"
        sort_dic["immunity"]       = 1
        sort_dic["brain"]          = 2
        sort_dic["energy"]         = 3
        sort_dic["eyes"]           = 4
        sort_dic["heart"]          = 5
        sort_dic["digestion"]      = 6
        sort_dic["bones"]          = 7
        sort_dic["fitness"]        = 8
        sort_dic["new"]            = True
        sort_dic["all"]            = ""

        categories = [categories for categories in Category.objects.filter(name__contains=sort_dic[sort])]
        if categories:
            for category in categories: #category_all
                context["id"]                         = category.id
                context["subcategory"]                = {}
                context["subcategory"]["title"]       = category.name
                context["subcategory"]["description"] = category.description
                
                products = Product.objects.filter(category=category)    #products_category for product_category in products_category
                
               #product_info_list
                for product in products:
                    goals = product.goal.all()      #goals_product      for goal_product in goals_product
                    product_stocks = product.productstock_set.all()     #product_SSPs     for product_SSP in product_SSPs 알아맞춰봥
                    goal_name_list = [goal.name for goal in goals]
                    product_stock_price_list = [product_stock.price for product_stock in product_stocks] #product_price_list
                    product_stock_count_list = [product_stock.stock for product_stock in product_stocks] #product_stock_list
                    product_stock_size_list  = [product_stock.size for product_stock in product_stocks]
                    is_soldout = True if sum(product_stock_count_list) == 0 else False

                    product_info = {}#product_info
                    product_info["id"]           = product.id
                    product_info["displayTitle"] = product.name
                    product_info["subTitle"]     = product.sub_name
                    product_info["imageUrl"]     = product.image_set.get(is_main=True).image_url
                    product_info["symbolURL"]    = goal_name_list
                    product_info["description"]  = product.description
                    product_info["displayPrice"] = product_stock_price_list
                    product_info["displaySize"]  = product_stock_size_list
                    product_info["isNew"]        = product.is_new
                    product_info["isSoldout"]    = is_soldout
                    product_info_list.append(product_info)

                context["item"] = product_info_list
                result.append(context)

            return JsonResponse({"data": result, "message": "SUCCESS"}, status=200)

        else:
            products = Product.objects.filter(goal=sort_dic[sort]) or Product.objects.filter(is_new=sort_dic[sort])
            #recently added                 # 프론트에 얘기하기 
            #products = Product.objects.filter(is_new=True)
            for product in products:
                goals = product.goal.all()      #goals_product      for goal_product in goals_product
                product_stocks = product.productstock_set.all()     #product_SSPs     for product_SSP in product_SSPs 알아맞춰봥
                goal_name_list = [goal.name for goal in goals]
                product_stock_price_list = [product_stock.price for product_stock in product_stocks] #product_price_list
                product_stock_count_list = [product_stock.stock for product_stock in product_stocks] #product_stock_list
                product_stock_size_list  = [product_stock.size for product_stock in product_stocks]
                is_soldout = True if sum(product_stock_count_list) == 0 else False

                product_info["id"]           = product.id
                product_info["displayTitle"] = product.name
                product_info["subTitle"]     = product.sub_name
                product_info["imageUrl"]     = product.image_set.get(is_main=True).image_url
                product_info["symbolURL"]    = goal_name_list
                product_info["description"]  = product.description
                product_info["displayPrice"] = product_stock_price_list
                product_info["displaySize"]  = product_stock_size_list
                product_info["isNew"]        = product.is_new
                product_info["isSoldout"]    = is_soldout
                product_info_list.append(product_info)

                context["item"] = product_info_list

            return JsonResponse({"data": result, "message": "SUCCESS"}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message': 'DOES_NOT_EXIST'}, status=404)
        
        product  = Product.objects.get(id=product_id)
        category = product.category.menu.name
        
        # is_vegan, is_vegeterian
        vegan_level = product.vegan_level_id
        if vegan_level == 1:
            is_vegan      = True
            is_vegeterian = False
        elif vegan_level == 2:
            is_vegan      = False
            is_vegeterian = True
        else:
            is_vegan      = False
            is_vegeterian = False

        # size, price
        product_SSPs = ProductStock.objects.filter(product=product)  # SSP: size, stock, price
        if category == 'vitamins':
            price      = product_SSPs[0].price   
            is_soldout = True if product_SSPs[0].stock == 0 else False 
        else:
            price = {
                product_SSPs[0].size : product_SSPs[0].price,
                product_SSPs[1].size : product_SSPs[1].price
            }
            is_soldout = {
                product_SSPs[0].size : True if product_SSPs[0].stock == 0 else False,
                product_SSPs[1].size : True if product_SSPs[1].stock == 0 else False,
            }

        # similar products
        similar_product_list = []
        goals_product        = product.goal.all()
        for goal_product in goals_product:
            similar_products = goal_product.product_set.exclude(id=product_id)
            
            for similar_product in similar_products:
                similar_product_info = {
                        'id'             : similar_product.id,
                        'title'          : similar_product.name,
                        'subTitle'       : similar_product.sub_name,
                        'imageUrl'       : similar_product.image_set.get(is_main=True).image_url,
                        'healthGoalList' : [goal.name for goal in similar_product.goal.all()]
                }
                similar_product_list.append(similar_product_info)
        
        context = {}
        context['category']            = category 
        context['productImageSrc']     = product.image_set.get(is_main=False).image_url
        context['productCardImageSrc'] = product.image_set.get(is_main=True).image_url
        context['isVegan']             = is_vegan
        context['isVegetarian']        = is_vegeterian
        context['healthGoalList']      = [goal.name for goal in product.goal.all()]
        context['title']               = product.name
        context['subTitle']            = product.sub_name
        context['description']         = product.description
        context['nutritionLink']       = product.nutrition_url
        context['allergyList']         = [allergy.name for allergy in product.allergy.all()]
        context['productPrice']        = price
        context['isSoldOut']           = is_soldout
        context['dietaryHabitList']    = [dietary_habit.name for dietary_habit in product.dietary_habit.all()]
        context['similarProduct']      = similar_product_list[:2] 
        
        return JsonResponse({"data": context, "message": "SUCCESS"}, status=200)

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