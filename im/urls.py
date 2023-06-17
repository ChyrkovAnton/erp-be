from django.urls import path
from .views import GoodsCategoriesAPIView, GoodsCategoriesAPIViewTree, GoodsAPIView


urlpatterns = [
    path('categories/', GoodsCategoriesAPIView.as_view()),
    path('categories_tree/', GoodsCategoriesAPIViewTree.as_view()),
    path('goods/', GoodsAPIView.as_view()),
]