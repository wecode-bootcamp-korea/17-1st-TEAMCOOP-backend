from django.urls import path
from .views      import ProductToCartView 

urlpatterns = [
    path('/tocart', ProductToCartView.as_view()), 
]
