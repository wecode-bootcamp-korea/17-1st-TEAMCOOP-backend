import json

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.utils     import login_decorator
from product.models import Product, Disease, Allergy, Goal
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
                
                if answer["id"] in [1, 3, 4]:
                    one_answer_list = [value for key, value in answer.items() if key != 'id']
                else:
                    one_answer_list = [key for key, value in answer.items() if value and key != 'id']
                all_answer.append(one_answer_list)
            
            answer = {
                {"id":1, "name":"wecode"},
                {"id":2, "male": 0, "female": 1},
                {"id":3, "age": 0 if age>50 else 1},
                {"id":4, "height": int, "weight": int},
                {"id":5, "workLess3hours": 0, "workLess6hours": 1, "workMore6hours": 2},
                {"id":6, "yesSmoke": 0, "noSmoke": 1},
                {"id":7, "drinkingLess": 0, "drinkingMore": 1},
                {"id":8, "Immunity": bool,"Brain": bool,"Energy": bool,"Eyes": bool,"Heart": bool,"Digestion": bool,"Bones": bool,"Fitness": bool},
                {"id":9, "vegan": bool, "vegetarian": bool, "nonVegetarian": bool},
                {"id":10, "soy": bool, "nuts": bool, "milk": bool, "milk": bool, "wheat": bool, "fish": bool},
                {"id":11, "arthritis": bool, "diabetes": bool, "menstrualIrregularity": bool, "liverDisease": bool, "osteoporosis": bool}
            }

            gender       = all_answer[1][0]
            age          = int(all_answer[2][0])
            height       = int(all_answer[3][0])
            weight       = int(all_answer[3][1])
            activity     = all_answer[4][0]
            care_smoker  = all_answer[5][0]
            care_drinker = all_answer[6][0]
            goals        = all_answer[7]
            vegan_type   = all_answer[8][0]
            allergies    = all_answer[9]
            diseases     = all_answer[10]

            gender_code     = [1, 3] if gender == 'male' else [2, 3]
            age_code        = [2, 3] if age >= 50 else [1, 3]
            bmi             = weight/((height*0.01)**2)
            care_obesity    = [0, 1] if  bmi>= 25 else [0]
            activity_level  = [3] if activity == 'workoutMore6hours' else [1,2]
            care_smoker     = bool(care_smoker == 'yesSmoke')
            care_drinker    = [0, 1] if care_drinker == 'drinkingMore' else [0]
            goal_id_list    = [goal.id for goal in Goal.objects.filter(name__in=goals)]
            vegan_level     = {vegan_type == 'vegan': [1], vegan_type == 'vegetarian': [1, 2]}.get(True, [1, 2 ,3])
            allergy_id_list = [allergy.id for allergy in Allergy.objects.filter(name__in=allergies)]
            disease_id_list = [disease.id for disease in Disease.objects.filter(name__in=diseases)]
            
            q = Q()
            q.add(Q(gender_code__in = gender_code) & Q(age_level__in = age_code) 
                & Q(care_obesity__in = care_obesity) & Q(activity_level__in = activity_level) 
                & Q(care_smoker = care_smoker) & Q(care_drinker__in = care_drinker) 
                & Q(goal__in = goal_id_list) & Q(vegan_level__in = vegan_level), q.OR)

            if allergy_id_list:
                q.add(~Q(allergy__in = allergy_id_list), q.AND)

            if disease_id_list:
                q.add(Q(disease__in = disease_id_list), q.AND)

            results_products = Product.objects.filter(q | Q(is_default=True)).distinct()
                      
            if QuizResult.objects.filter(user=user):
                user.recommendation.clear()
            
            recommendations = []
            for result_product in results_products:
                user.recommendation.add(result_product)

                product_SSPs   = result_product.productstock_set.all()
                price_list     = [product_SSP.price for product_SSP in product_SSPs] #product_price_list
                size_list      = [product_SSP.size for product_SSP in product_SSPs]
                goals          = result_product.goal.all()
                goal_name_list = [goal.name for goal in goals]

                product_info = {
                "id"         : result_product.id,
                "title"      : result_product.name,
                "subTitle"   : result_product.sub_name,
                "imageUrl"   : result_product.image_set.get(is_main=True).image_url,
                "healthGoal" : goal_name_list,
                "price"      : price_list,
                "size"       : size_list
                }


                recommendations.append(product_info)

            return JsonResponse({'data':recommendations, 'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

