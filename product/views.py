import json
from datetime import datetime
from random   import randint

from django.http            import JsonResponse, HttpResponse, Http404
from django.views           import View
from django.db.models       import Q

from user.utils     import login_decorator
from product.models import Category, Product, ProductStock, Goal

class ProductListView(View):
    def make_product_info_list(self, products):
        product_info_list  = [
                {
                          "id"           : product.id,
                          "displayTitle" : product.name,
                          "subTitle"     : product.sub_name,
                          "imageUrl"     : product.image_set.get(is_main=True).image_url,
                          "symbolURL"    : [goal.name for goal in product.goal.all()],
                          "description"  : product.description,
                          "displayPrice" : [product_stock.price for product_stock in product.productstock_set.all()],
                          "displaySize"  : [product_stock.stock for product_stock in product.productstock_set.all()],
                          "isNew"        : product.is_new,
                          "isSoldout"    : bool(sum(product_stock.stock for product_stock in product.productstock_set.all()))
                          } for product in products]

        return product_info_list

    def get(self, request):
        sort = request.GET.get('sort', None)
        q=Q()
        if sort:
            q.add(Q(name__icontains=sort),q.OR)
        categories = Category.objects.filter(q)

        if categories.exists(): 
            result = [{
                    "id"          : category.id,
                    "subcategory" : {
                        "title"       : category.name,
                        "description" : category.description,
                    },
                    "item"        : self.make_product_info_list(products=Product.objects.filter(category=category)) 
                } for category in categories]

            return JsonResponse({"data": result, "message": "SUCCESS"}, status=200)

        if Goal.objects.filter(name__icontains=sort).exists():
            products = Product.objects.filter(goal=Goal.objects.get(name__icontains=sort))
            result   = self.make_product_info_list(products=products) 
            
            return JsonResponse({"data": result, "message": "SUCCESS"}, status=200)

        if sort == 'new':
            products = Product.objects.filter(is_new=bool(sort == 'new'))
            result   = self.make_product_info_list(products=products) 

            return JsonResponse({"data": result, "message": "SUCCESS"}, status=200)

        return JsonResponse({"message": "PAGE_NOT_FOUND"}, status=404)

        
class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product  = Product.objects.get(id=product_id)
            category_name = product.category.menu.name
            context  = {
                'category'           : category_name,
                'id'                 : product.id,
                'productImageSrc'    : product.image_set.get(is_main=False).image_url,
                'productCardImageSrc': product.image_set.get(is_main=True).image_url,
                'healthGoalList'     : [goal.name for goal in product.goal.all()],
                'title'              : product.name,
                'subTitle'           : product.sub_name,
                'description'        : product.description,
                'nutritionLink'      : product.nutrition_url,
                'allergyList'        : [allergy.name for allergy in product.allergy.all()],
                'dietaryHabitList'   : [dietary_habit.name for dietary_habit in product.dietary_habit.all()],
                }

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

            context['isVegan']        = is_vegan
            context['isVegetarian']   = is_vegeterian

        # size, price
            product_SSPs = ProductStock.objects.filter(product=product)  # SSP: siz e, stock, price
            if category_name == 'vitamins':
                price      = product_SSPs.first().price   
                is_soldout = product_SSPs.first().stock == 0
            else:
                price      = {product_SSP.size : product_SSP.price for product_SSP in product_SSPs}
                is_soldout = {product_SSP.size : product_SSP.stock == 0 for product_SSP in product_SSPs}
            context['productPrice']     = price
            context['isSoldOut']        = is_soldout

        # similar products
            for goal_product in product.goal.all():
                similar_product_list = [
                    {
                        'id'            : similar_product.id,
                        'title'         : similar_product.name,
                        'subTitle'      : similar_product.sub_name,
                        'imageUrl'      : similar_product.image_set.get(is_main=True).image_url,
                        'healthGoalList': [goal.name for goal in similar_product.goal.all()],
                    }
                    for similar_product in goal_product.product_set.exclude(id=product_id)]

                context['similarProduct'] = similar_product_list[:2] 

            return JsonResponse({"data": context, "message": "SUCCESS"}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message": "BAD_REQUEST"}, status=400) 