from .models import Good, GoodsFeature
from rest_framework.utils import json


def get_goods_queryset_filtered_by_category(request):
    category = request.GET.get('category_id')
    if category:
        if category == '1':
            return Good.objects.all()
        return Good.objects.filter(good_category=int(category))
    return []


def get_goods_queryset_bound_by_price(request, queryset):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        goods_ids = []
        for good in queryset:
            if float(min_price) <= float(get_current_price(good)) <= float(max_price):
                goods_ids.append(good.id)
        return queryset.filter(id__in=goods_ids)
    return queryset


def get_goods_queryset_filtered_by_features(request, queryset):
    features_ids = get_features(request)
    grouped_features = group_features_by_type(features_ids)
    filtered_goods = queryset
    if len(grouped_features) > 0:
        for group in grouped_features:
            print(group['features'])
            goods_ids = []
            for good in filtered_goods:
                good_features = good.goodsfeature_set.filter(id__in=group['features'])
                if len(good_features) > 0:
                    goods_ids.append(good.id)
            filtered_goods = queryset.filter(id__in=goods_ids)
    return filtered_goods


def get_current_price(good):
    prices = good.prices.all()
    if prices:
        return str(prices.filter(price_type='1').order_by('-price_date').first().value)
    return '0.00'


def get_price_range(goods):
    if len(goods) == 0:
        return {'min_price': 0, 'max_price': 0}
    prices = []
    for good in goods:
        prices.append(float(get_current_price(good)))
    return {'min_price': min(prices), 'max_price': max(prices)}


def get_distinct_characteristics_list(queryset):
    characteristic_list = []
    for good in queryset:
        for feature in good.goodsfeature_set.all():
            if feature not in characteristic_list:
                characteristic_list.append(feature)
    return characteristic_list


def get_distinct_characteristic_types(queryset):
    characteristic_list = get_distinct_characteristics_list(queryset)
    characteristic_types = []
    for char in characteristic_list:
        characteristic = {'id': char.characteristic_type.id,
                          'name': char.characteristic_type.characteristic_full_name,
                          'priority': char.characteristic_type.priority,
                          'uom': char.uom.uom_short_name}
        if characteristic not in characteristic_types:
            characteristic_types.append(characteristic)
    return characteristic_types


def get_characteristics_filters(characteristic_list, characteristic_types, category):
    characteristics = []
    for ch_type in characteristic_types:
        values = [{'value': char.characteristic_value,
                   'id': char.id,
                   'count': char.good.filter(good_category=category).count()}
                  for char in characteristic_list
                  if char.characteristic_type.id == ch_type['id']]
        characteristics.append({'characteristic': ch_type,
                                'values': values})
    return characteristics


def create_category_characteristics_response(request):
    category = request.GET.get('category_id')
    category_goods = get_goods_queryset_filtered_by_category(request)
    goods_list = get_goods_queryset_bound_by_price(request, category_goods)
    char_list = get_distinct_characteristics_list(goods_list)
    dist_char_types = get_distinct_characteristic_types(goods_list)
    char_filters = get_characteristics_filters(char_list, dist_char_types, category)
    return {'characteristics': char_filters,
            'prices': get_price_range(category_goods)}


def get_active_features(request):
    active_category_goods = get_goods_queryset_filtered_by_category(request)
    ac_goods_bound_by_price = get_goods_queryset_bound_by_price(request, active_category_goods)
    ac_goods_bpp_filtered_by_features = get_goods_queryset_filtered_by_features(request, ac_goods_bound_by_price)
    features_rel = select_same_category_features(request, ac_goods_bound_by_price)
    active_features_ids = []
    active_features = []
    for good in ac_goods_bpp_filtered_by_features:
        for feature in good.goodsfeature_set.all():
            active_features_ids.append(feature.id)
    for feature in list(set(active_features_ids + features_rel)):
        count = 0
        for feature_id in active_features_ids + features_rel:
            if feature_id == feature:
                count += 1
        active_features.append({'id': feature, 'count': count})
    return {'active_features': active_features}


def select_same_category_features(request, queryset):
    # Selects other than those sent in request GoodsFeatures ids for Good queryset,
    # which have a feature type the same as the first feature from request has
    features_relatives = []
    features = get_features(request)
    if type(features) == list and len(features) > 0:
        first_feature = GoodsFeature.objects.get(id=features[0])
        feature_type_id = first_feature.characteristic_type.id
        for good in queryset:
            for feature in good.goodsfeature_set.all():
                if feature.characteristic_type.id == feature_type_id:
                    features_relatives.append(feature.id)
    for feature in features:
        if feature in features_relatives:
            features_relatives.remove(feature)
    return features_relatives


def get_features(request):
    # Returns either array of features sent in request, or an empty array if
    # the request does not contain "features" parameter
    features_raw = request.GET.get('features')
    if features_raw:
        return json.loads(features_raw)
    return []


def group_features_by_type(features_array):
    goods_features = GoodsFeature.objects.filter(id__in=features_array)
    features_types = []
    for feature in goods_features:
        if feature.characteristic_type.id not in features_types:
            features_types.append(feature.characteristic_type.id)
    features_by_type = []
    for feature_type in features_types:
        type_features = goods_features.filter(characteristic_type=feature_type)
        features_ids = [feature.id for feature in type_features]
        features_by_type.append({
            'type': feature_type,
            'features': features_ids
        })
    return features_by_type


