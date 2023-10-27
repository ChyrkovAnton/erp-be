from django.urls import path
from .views import GoodsCategoriesAPIView, GoodsCategoriesAPIViewTree, \
    GoodsAPIView, UoMAPIView, GoodCharacteristicTypeAPIView, \
    GoodsCharacteristicAPIView, send_category_characteristics, \
    get_filtered_goods_list, GoodsFeatureAPIView, send_active_features, \
    send_goods_pivot, make_goods_grouped_by_category_name_response, GoodAPIView, \
    WishListGoodsAPIView


urlpatterns = [
    path('categories/', GoodsCategoriesAPIView.as_view()),
    path('categories_tree/', GoodsCategoriesAPIViewTree.as_view()),
    path('goods/', GoodsAPIView.as_view()),
    path('goods/<int:good_id>/', GoodAPIView.as_view()),
    path('filtered_goods/', get_filtered_goods_list),
    path('uoms/', UoMAPIView.as_view()),
    path('good_char_types/', GoodCharacteristicTypeAPIView.as_view()),
    path('good_charact/', GoodsCharacteristicAPIView.as_view()),
    path('good_features/', GoodsFeatureAPIView.as_view()),
    path('category_characteristics/', send_category_characteristics),
    path('active_features/', send_active_features),
    path('goods_pivot/', send_goods_pivot),
    path('goods_by_category/', make_goods_grouped_by_category_name_response),
    path('wish_list/', WishListGoodsAPIView.as_view()),
]