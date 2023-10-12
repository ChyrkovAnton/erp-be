from .models import Good, GoodsFeature
from rest_framework.utils import json
import pandas as pd


def filter_goods_by_category(request):
    category = request.GET.get('category_id')
    if category:
        if category == '1':
            return Good.objects.all()
        return Good.objects.filter(good_category=int(category))
    return []


def filter_goods_by_price(request, queryset):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        goods_ids = []
        for good in queryset:
            if float(min_price) <= float(get_current_price(good)) <= float(max_price):
                goods_ids.append(good.id)
        return queryset.filter(id__in=goods_ids)
    return queryset


def filter_goods_by_features(request, queryset, *features_array):
    features_ids = get_features(request)
    if features_array:
        features_ids = features_array[0]
    grouped_features = group_features_by_type(features_ids)
    if len(grouped_features) > 0:
        for group in grouped_features:
            goods_ids = []
            for good in queryset:
                good_features = good.goodsfeature_set.filter(id__in=group['features'])
                if len(good_features) > 0:
                    goods_ids.append(good.id)
        return queryset.filter(id__in=goods_ids)
    return queryset


def filter_goods_by_all_parameters(request):
    goods_list_raw = request.GET.get('good_ids')
    if goods_list_raw is not None:
        goods_list = json.loads(goods_list_raw)
        return Good.objects.filter(id__in=goods_list)
    goods_filtered_by_category = filter_goods_by_category(request)
    goods_filtered_by_price = filter_goods_by_price(request, goods_filtered_by_category)
    return filter_goods_by_features(request, goods_filtered_by_price)


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
    category_goods = filter_goods_by_category(request)
    goods_list = filter_goods_by_price(request, category_goods)
    char_list = get_distinct_characteristics_list(goods_list)
    dist_char_types = get_distinct_characteristic_types(goods_list)
    char_filters = get_characteristics_filters(char_list, dist_char_types, category)
    return {'characteristics': char_filters,
            'prices': get_price_range(category_goods)}


def get_active_features(request):
    goods = filter_goods_by_all_parameters(request)
    clear_array = clear_current_features_array(get_features(request))
    features_last_type = get_last_type_features(request, clear_array)
    active_features_ids = []
    active_features = []
    for good in goods:
        for feature in good.goodsfeature_set.all():
            active_features_ids.append(feature.id)
    for feature in list(set(active_features_ids + features_last_type)):
        count = 0
        for feature_id in active_features_ids + features_last_type:
            if feature_id == feature:
                count += 1
        active_features.append({'id': feature, 'count': count})
    return {'active_features': active_features}


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


def clear_current_features_array(features_array):
    # Removes all the features with the last chosen feature type from the feature array
    if len(features_array) > 0:
        last_chosen_feature_id = features_array[-1]
        last_chosen_feature = GoodsFeature.objects.get(id=last_chosen_feature_id)
        last_chosen_feature_type_id = last_chosen_feature.characteristic_type.id
        features = GoodsFeature.objects.filter(id__in=features_array)
        return [feature.id for feature in features
                if feature.characteristic_type.id != last_chosen_feature_type_id]


def get_last_type_features(request, features_array):
    features = get_features(request)
    if len(features) > 0:
        last_chosen_feature = GoodsFeature.objects.get(id=features[-1])
        last_chosen_feature_type_id = last_chosen_feature.characteristic_type.id
        active_category_goods = filter_goods_by_category(request)
        ac_goods_bound_by_price = filter_goods_by_price(request, active_category_goods)
        goods_filt_by_features = filter_goods_by_features(request, ac_goods_bound_by_price, features_array)
        last_type_features_ids = []
        for good in goods_filt_by_features:
            for feature in good.goodsfeature_set.all():
                if feature.characteristic_type.id == last_chosen_feature_type_id:
                    if feature.id not in features:
                        last_type_features_ids.append(feature.id)
        return last_type_features_ids
    return []


def pivot_goods_features(request):
    goods = get_goods_by_id_list(request)
    plain_goods = []
    for good in goods:
        plain_good = {'image': build_absolute_uri_good_image(request, good.good_image.__str__()),
                      'name': [good.id, good.name],
                      'price': get_current_price(good)}
        for feature in good.goodsfeature_set.all():
            feature_repr = f'{feature.characteristic_type.characteristic_full_name}, {feature.uom.uom_short_name}'
            plain_good.update({feature_repr: feature.characteristic_value})
        plain_goods.append(plain_good)
    df = pd.DataFrame(plain_goods)
    df = df.transpose().fillna('')
    return df.to_dict('split')


def build_absolute_uri_good_image(request, image_uri):
    return f'http://{request.get_host()}/media/{image_uri}'


def group_goods_by_category_name(request):
    goods = get_goods_by_id_list(request)
    categories = list(set([good.good_category.name for good in goods]))
    return ([{'category_name': category,
             'goods': [good.id for good in goods.filter(good_category__name=category)]}
            for category in categories])


def get_goods_by_id_list(request):
    good_ids_parameter = request.GET.get('good_ids')
    good_ids = json.loads(good_ids_parameter)
    if isinstance(good_ids, list):
        return Good.objects.filter(id__in=good_ids)


def get_wish_list_goods(request):
    wish_list_raw = request.GET.get('wish_list')
    if wish_list_raw is not None:
        goods_list = json.loads(wish_list_raw)
        return Good.objects.filter(id__in=goods_list)