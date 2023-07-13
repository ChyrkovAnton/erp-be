from django.urls import path
from .views import GoodsCategoriesAPIView, GoodsCategoriesAPIViewTree, \
    GoodsAPIView, UoMAPIView, GoodCharacteristicTypeAPIView, \
    GoodsCharacteristicAPIView


urlpatterns = [
    path('categories/', GoodsCategoriesAPIView.as_view()),
    path('categories_tree/', GoodsCategoriesAPIViewTree.as_view()),
    path('goods/', GoodsAPIView.as_view()),
    path('uoms/', UoMAPIView.as_view()),
    path('good_char_types/', GoodCharacteristicTypeAPIView.as_view()),
    path('good_charact/', GoodsCharacteristicAPIView.as_view()),
]