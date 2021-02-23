from django.urls   import path
from product.views import ProductView, GoalView, ProductToCartView, ProductDetailView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/category/<int:id>', ProductView.as_view()),
    path('/goal/<int:id>', GoalView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/tocart', ProductToCartView.as_view()),
]