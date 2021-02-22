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
        result = []
        # show_all
        if id == None:
            categorie_all = Category.objects.all() 
            for category in category_all: 
                context = {}
                context["id"] = category.id
                context["subcategory"] = {}
                context["subcategory"]["title"] = category.name
                context["subcategory"]["description"] = category.description
                
                products_category = Product.objects.filter(category=category)    #products_category for product_category in products_category
                
                product_info_list = []   #product_info_list
                for product_category in products_category:
                    goals_product      = product.goal.all()      #goals_product      for goal_product in goals_product
                    product_SSPs       = product.productstock_set.all()     #product_SSPs     for product_SSP in product_SSPs 알아맞춰봥
                    goal_name_list     = [goal_product.name for goal_product in goals_product]
                    product_price_list = [product_SSP.price for product_SSP in product_SSPs] #product_price_list
                    product_stock_list = [product_SSP.stock for product_SSP in product_SSPs] #product_stock_list
                    product_size_list  = [product_SSP.size for product_SSP in product_SSPs]
                    is_soldout         = bool(sum(product_stock_count_list) == 0)

                    product_info = {
                        "id"          : product.id,
                        "displayTitle": product_category.name, 
                        "subTitle"    : product_category.sub_name,
                        "imageUrl"    : product_category.image_set.get(is_main=True).image_url,  
                        "symbolURL"   : goal_name_list,             
                        "description" : product_category.description,
                        "displayPrice": product_price_list, 
                        "displaySize" : product_size_list,
                        "isNew"       : product_category.is_new,
                        "isSoldout"   : is_soldout
                    }
                    product_info_list.append(product_info)

                context["item"] = product_info_list
                result.append(context)

            return JsonResponse({"data": result, "message": "SUCCESS"}, status=200)
        
        #recently added  
        if id == 99999:            
            products = Product.objects.filter(is_new=True)
            for product in products:
                goals_product = product.goal.all()
                product_SSPs  = product.productstock_set.all()

                product_price_list = [product_SSP.price for product_SSP in product_SSPs]
                product_stock_list = [product_SSP.stock for product_SSP in product_SSPs] 
                product_size_list  = [product_SSP.size for product_SSP in product_SSPs]
                goal_name_list     = [goal_product.name for goal_product in goals_product]
                is_soldout         = bool(sum(product_stock_count_list) == 0)
                product_info = {
                        "id"          : product.id,
                        "displayTitle": product.name, 
                        "subTitle"    : product.sub_name,
                        "imageUrl"    : product.image_set.get(is_main=True).image_url, 
                        "symbolURL"   : goal_name_list,               
                        "description" : product.description,
                        "displayPrice": product_price_list,
                        "displaySize" : product_size_list,
                        "isNew"       : product.is_new,
                        "isSoldout"   : is_soldout
                        }
                
                result.append(product_info)
            
            return JsonResponse({"data": result, "message": "SUCCESS"}, status=200)
        
        #카테고리별 상품보기
        if Category.objects.filter(id=id).exists:
            categories = Category.objects.filter(id=id)
            for category in categories:
                context = {}
                context["id"] = category.id
                context["subcategory"] = {}
                context["subcategory"]["title"] = category.name
                context["subcategory"]["description"] = category.description
                
                products_category = Product.objects.filter(category=category)
                product_info_list = []
                for product_category in products_category:
                    goals_product = product.goal.all()
                    product_SSPs  = product.productstock_set.all()

                    product_price_list = [product_SSP.price for product_SSP in product_SSPs]
                    product_stock_list = [product_SSP.stock for product_SSP in product_SSPs]
                    product_size_list  = [product_SSP.size for product_SSP in product_SSPs]
                    goal_name_list     = [goal_product.name for goal_product in goals_product]
                    is_soldout         = bool(sum(product_stock_count_list) == 0)

                    product_info = {
                        "id"          : product_category.id,
                        "displayTitle": product_category.name, 
                        "subTitle"    : product_category.sub_name,
                        "imageUrl"    : product_category.image_set.get(is_main=True).image_url,  
                        "symbolURL"   : goal_name_list,              
                        "description" : product_category.description,
                        "displayPrice": product_price_list,
                        "displaySize" : product_size_list,
                        "isNew"       : product_category.is_new,
                        "isSoldout"   : is_soldout
                        }
                    product_info_list.append(product_info)

                context["item"] = product_info_list
                result.append(context)
            
            return JsonResponse({"data": result, "message": "SUCCESS"}, status=200)
        
                    
class GoalView(View):
    def get(self, request, id):
        result = []
        if Goal.objects.filter(id=id):
            # product_result = []
            products = Product.objects.filter(goal=Goal.objects.get(id=id).id)
            for product in products:
                goals_product = product.goal.all()
                product_SSPs = product.productstock_set.all()

                product_price_list = [product_SSP.price for product_SSP in product_SSPs]
                product_stock_list = [product_SSP.stock for product_SSP in product_SSPs]
                product_size_list  = [product_SSP.size for product_SSP in product_SSPs]
                goal_name_list     = [goal_product.name for goal_product in goals_product]
                is_soldout         = bool(sum(product_stock_count_list) == 0)

                product_info = {
                        "id"           : product.id,
                        "displayTitle" : product.name, 
                        "subTitle"     : product.sub_name,
                        "imageUrl"     : product.image_set.get(is_main=True).image_url,   #나중에 수정해야함 is_main
                        "symbolURL"    : goal_name_list,            
                        "description"  : product.description,
                        "displayPrice" : product_price_list,
                        "displaySize"  : product_size_list,
                        "isNew"        : product.is_new,
                        "isSoldout"    : is_soldout
                        }
                
                result.append(product_info)

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
            is_soldout = bool(product_SSPs[0].stock == 0)
        else:
            price = {
                product_SSPs[0].size : product_SSPs[0].price,
                product_SSPs[1].size : product_SSPs[1].price
            }
            is_soldout = {
                product_SSPs[0].size : bool(product_SSPs[0].stock == 0),
                product_SSPs[1].size : bool(product_SSPs[1].stock == 0)
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
        