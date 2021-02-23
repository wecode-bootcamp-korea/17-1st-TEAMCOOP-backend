from django.urls import path
from .views      import CartView

urlpatterns = [
    path('/mycart', CartView.as_view()),
]
