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