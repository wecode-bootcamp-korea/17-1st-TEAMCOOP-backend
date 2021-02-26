from django.urls   import path
from product.views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]