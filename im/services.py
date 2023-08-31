from .models import Good, GoodsCharacteristic, GoodsFeature


def get_goods_queryset_filtered_by_category(request):
    category = request.GET.get('category_id')
    return Good.objects.filter(good_category=int(category))


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


# def get_category_goods_characteristics(request):
#     goods_list = [good.public_id for good in get_goods_queryset_bound_by_price(
#         request, get_goods_queryset_filtered_by_category(request))]
#     goods_characteristics = GoodsCharacteristic.objects.filter(good__public_id__in=goods_list)
#     goods_characteristics_list = [{'id': characteristic.characteristic_type.id,
#                                    'name': characteristic.characteristic_type.characteristic_full_name,
#                                    'uom': characteristic.uom.uom_short_name}
#                                   for characteristic in goods_characteristics]
#
#     def get_unique_characteristics_list(full_characteristics_list):
#         if len(goods_characteristics_list) == 0:
#             return []
#         unique_characteristics_list = [full_characteristics_list[0]]
#         for characteristic in goods_characteristics_list:
#             if characteristic not in unique_characteristics_list:
#                 unique_characteristics_list.append(characteristic)
#         return unique_characteristics_list
#
#     def get_unique_characteristics_list_with_values(unique_characteristics_list, characteristics_list):
#         unique_characteristics_list_with_values = []
#         for characteristic in unique_characteristics_list:
#             characteristic_values = [value["characteristic_value"]
#                                      for value in characteristics_list
#                                      if value["characteristic_type_id"] == characteristic['id']]
#             unique_characteristics_list_with_values.append({'characteristic': characteristic,
#                                                             'values': list(set(characteristic_values))})
#         return unique_characteristics_list_with_values
#     return get_unique_characteristics_list_with_values(get_unique_characteristics_list(goods_characteristics_list),
#                                                        goods_characteristics.values())


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


def get_characteristics_list(queryset):
    characteristic_list = []
    for good in queryset:
        for feature in good.goodsfeature_set.all():
            characteristic_list.append(feature)
    return characteristic_list


def get_distinct_characteristic_types(queryset):
    characteristic_list = get_characteristics_list(queryset)
    characteristic_types = []
    for char in characteristic_list:
        characteristic = {'id': char.characteristic_type.id,
                          'name': char.characteristic_type.characteristic_full_name,
                          'priority': char.characteristic_type.priority,
                          'uom': char.uom.uom_short_name}
        if characteristic not in characteristic_types:
            characteristic_types.append(characteristic)
    return characteristic_types


def get_characteristics_filters(characteristic_list, characteristic_types):
    characteristics = []
    for ch_type in characteristic_types:
        values = [{'value': char.characteristic_value} for char in characteristic_list
                  if char.characteristic_type.id == ch_type['id']]
        characteristics.append({'characteristic': ch_type,
                                'values': values})
    return characteristics


def create_category_characteristics_response(request):
    category_goods = get_goods_queryset_filtered_by_category(request)
    goods_list = get_goods_queryset_bound_by_price(request, category_goods)
    char_list = get_characteristics_list(goods_list)
    dist_char_types = get_distinct_characteristic_types(goods_list)
    char_filters = get_characteristics_filters(char_list, dist_char_types)
    return {'characteristics': char_filters,
            'prices': get_price_range(category_goods)}