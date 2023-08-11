from .models import Good, GoodsCharacteristic


def get_category_goods(request):
    category = request.GET.get('category_id')
    return Good.objects.filter(good_category=int(category))


def get_category_goods_characteristics(request):
    goods_list = [good.public_id for good in get_category_goods(request)]
    goods_characteristics = GoodsCharacteristic.objects.filter(good__public_id__in=goods_list)
    goods_characteristics_list = [{'id': characteristic.characteristics_type.id,
                                   'name': characteristic.characteristics_type.characteristics_full_name,
                                   'uom': characteristic.uom.uom_short_name}
                                  for characteristic in goods_characteristics]

    def get_unique_characteristics_list(full_characteristics_list):
        if len(goods_characteristics_list) == 0:
            return []
        unique_characteristics_list = [full_characteristics_list[0]]
        for characteristic in goods_characteristics_list:
            if characteristic not in unique_characteristics_list:
                unique_characteristics_list.append(characteristic)
        return unique_characteristics_list

    def get_unique_characteristics_list_with_values(unique_characteristics_list, characteristics_list):
        unique_characteristics_list_with_values = []
        for characteristic in unique_characteristics_list:
            characteristic_values = [value["characteristics_value"]
                                     for value in characteristics_list
                                     if value["characteristics_type_id"] == characteristic['id']]
            unique_characteristics_list_with_values.append({'characteristic': characteristic,
                                                            'values': list(set(characteristic_values))})
        return unique_characteristics_list_with_values
    return get_unique_characteristics_list_with_values(get_unique_characteristics_list(goods_characteristics_list),
                                                       goods_characteristics.values())


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
        prices.append(get_current_price(good))
    return {'min_price': min(prices), 'max_price': max(prices)}
