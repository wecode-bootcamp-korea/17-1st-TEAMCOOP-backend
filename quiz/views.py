import json

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

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
from .models        import QuizResult 

class RecommendationView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            answers = data['answer']
            
            all_answer = []
            for answer in answers:
                one_answer_list = []
                
                if answer["id"] in [1, 3, 4]:
                    one_answer_list = [value for key, value in answer.items() if key != 'id']
                else:
                    one_answer_list = [key for key, value in answer.items() if value and key != 'id']
                all_answer.append(one_answer_list)
            print("========start============") 
            print(all_answer)
            
            gender = all_answer[1][0]
            age = int(all_answer[2][0])
            bmi = int(all_answer[3][0])
            activity = all_answer[4][0]
            care_smoker = all_answer[5][0]
            care_drinker = all_answer[6][0]

            goals = all_answer[7]
            vegan_type = all_answer[8][0]
            allergies = all_answer[9]
            diseases = all_answer[10]

            gender_code = [1, 3] if gender == 'male' else [2, 3] 
            age_code = [1, 2] if age >= 50 else [1, 3] 
            care_obesity = bool(bmi >= 25)
            activity_level = [3] if activity == 'workoutMore6hours' else [1,2] 
            care_smoker = bool(care_smoker == 'yesSmoke')
            care_drinker = bool(care_drinker == 'drinkingMore')
            vegan_level = {vegan_type == 'vegan': 1, vegan_type == 'vegetarian': 2}.get(True, 3)
            
            q = Q(is_default=True)
            q.add(Q(gender_code__in = gender_code) & Q(age_level__in = age_code) & Q(care_obesity = care_obesity) 
                & Q(activity_level__in = activity_level) & Q(care_smoker = care_smoker) & Q(care_drinker = care_drinker) 
                & Q(goal__in = goals) & Q(vegan_level = vegan_level) & ~Q(allergy__in = allergies) & Q(disease__in = diseases), q.OR)
            result_products = Product.objects.filter(q).distinct()
            recommendations = []
            for result_product in results_products:
                if QuizResult.objects.filter(user=user):
                    user.recommendation.clear()
                user.recommendation.add(result_product)

                product_SSPs   = result_product.productstock_set.all()
                price_list     = [product_SSP.price for product_SSP in product_SSPs] #product_price_list
                size_list      = [product_SSP.size for product_SSP in product_SSPs]
                goals          = result_product.goal.all()
                goal_name_list = [goal.name for goal in goals]

                product_info = {}
                product_info["id"]         = result_product.id
                product_info["title"]      = result_product.name
                product_info["subTitle"]   = result_product.sub_name
                product_info["imageUrl"]   = result_product.image_set.get(is_main=True).image_url
                product_info["healthGoal"] = goal_name_list
                product_info["price"]      = price_list
                product_info["size"]       = size_list

                recommendations.append(product_info)

            return JsonResponse({'data':recommendations, 'message':'SUCCESS'}, status=200)

            print(result_products)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

