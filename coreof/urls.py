from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('order', include('order.urls')),
    path('recommendation', include('quiz.urls')),
]
