from django.urls import path
from .views      import CartView, CartDetailView

urlpatterns = [
    path('/mycart', CartView.as_view()),
    path('/cart/<int:product_stock_id>', CartDetailView.as_view()),
]
