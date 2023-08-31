from django.urls import path
from .views import GoodsCategoriesAPIView, GoodsCategoriesAPIViewTree, \
    GoodsAPIView, UoMAPIView, GoodCharacteristicTypeAPIView, \
    GoodsCharacteristicAPIView, get_category_characteristics, \
    get_filtered_goods_list, GoodsFeatureAPIView


urlpatterns = [
    path('categories/', GoodsCategoriesAPIView.as_view()),
    path('categories_tree/', GoodsCategoriesAPIViewTree.as_view()),
    path('goods/', GoodsAPIView.as_view()),
    path('filtered_goods/', get_filtered_goods_list),
    path('uoms/', UoMAPIView.as_view()),
    path('good_char_types/', GoodCharacteristicTypeAPIView.as_view()),
    path('good_charact/', GoodsCharacteristicAPIView.as_view()),
    path('good_features/', GoodsFeatureAPIView.as_view()),
    path('category_characteristics/', get_category_characteristics),
]