from django.urls import path
from .views      import CartView, CartDetailView, CheckOutView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/cart/<int:product_stock_id>', CartDetailView.as_view()),
    path('/checkout/<str:order_number>', CheckOutView.as_view()),
]
