from django.db.models import Sum, F
from user.models import User
from crm.models import OrderLine


def get_customer_statistics(request, **kwargs):
    POSITIVE_TRANSACTION_COLOR = 'green'
    NEGATIVE_TRANSACTION_COLOR = '#C0392B'
    statistics = []
    user = User.objects.get(public_id=kwargs['user'])
    # The total count of orders which have been ordered by the user
    user_orders = user.orders.all()
    statistics.append({'name': 'order_number',
                       'value': user_orders.count(),
                       'color': POSITIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна кількість замовлень',
                       'uom_ukr': 'шт.'})
    # The total count of orders which have been paid by the user
    paid_orders = user_orders.filter(is_paid=True)
    success_ord_count = {'name': 'successful_order_number',
                         'value': paid_orders.count(),
                         'color': POSITIVE_TRANSACTION_COLOR,
                         'title_ukr': 'Загальна кількість сплачених замовлень',
                         'uom_ukr': 'шт.'}
    statistics.append(success_ord_count)
    # The total count of orders which have been returned by the user
    returned_orders = user_orders.filter(is_returned=True)
    ret_ord_count = {'name': 'returned_order_number',
                     'value': returned_orders.count(),
                     'color': NEGATIVE_TRANSACTION_COLOR,
                     'title_ukr': 'Загальна кількість повернених замовлень',
                     'uom_ukr': 'шт.'}
    statistics.append(ret_ord_count)
    # The total count of orders which have been cancelled by the user
    cancelled_orders = user_orders.filter(is_cancelled=True)
    cnld_ord_count = {'name': 'cancelled_order_number',
                      'value': cancelled_orders.count(),
                      'color': NEGATIVE_TRANSACTION_COLOR,
                      'title_ukr': 'Загальна кількість скасованих замовлень',
                      'uom_ukr': 'шт.'}
    statistics.append(cnld_ord_count)
    # The total count of lines which have been ordered by the user
    user_orders_lines = OrderLine.objects.filter(order__in=user_orders)
    statistics.append({'name': 'order_lines_count',
                       'value': user_orders_lines.count(),
                       'color': POSITIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна кількість замовлених найменувань',
                       'uom_ukr': 'шт.'})
    # The total count of units which have been ordered by the user
    user_orders_units_count = user_orders_lines.aggregate(value=Sum('quantity'))
    statistics.append({'name': 'user_orders_units_count',
                       **user_orders_units_count,
                       'color': POSITIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна кількість замовлених одиниць товару',
                       'uom_ukr': 'шт.'})
    # The total price of units which have been ordered by the user
    user_orders_units_amount = user_orders_lines.aggregate(
        value=Sum(F('quantity') * F('price')))
    statistics.append({'name': 'orders_total',
                       **user_orders_units_amount,
                       'color': POSITIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна вартість сплачених замовлень',
                       'uom_ukr': 'грн'})
    # The total count of lines which have been paid by the user
    paid_user_orders_lines = OrderLine.objects.filter(order__in=paid_orders)
    statistics.append({'name': 'paid_user_orders_lines',
                       'value': paid_user_orders_lines.count(),
                       'color': POSITIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна кількість сплачених найменувань',
                       'uom_ukr': 'шт.'})
    # The total count of units which have been paid by the user
    paid_user_orders_units_count = paid_user_orders_lines.aggregate(value=Sum('quantity'))
    statistics.append({'name': 'paid_user_orders_units_count',
                       **paid_user_orders_units_count,
                       'color': POSITIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна кількість сплачених одиниць товару',
                       'uom_ukr': 'шт.'})
    # The total price of units which have been paid by the user
    paid_user_orders_units_amount = paid_user_orders_lines.aggregate(
        value=Sum(F('quantity') * F('price')))
    statistics.append({'name': 'paid_orders_total',
                       **paid_user_orders_units_amount,
                       'color': POSITIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна вартість сплачених замовлень',
                       'uom_ukr': 'грн'})
    # The total count of lines which have been cancelled by the user
    cancelled_user_orders_lines = OrderLine.objects.filter(order__in=cancelled_orders)
    statistics.append({'name': 'cancelled_user_orders_lines',
                       'value': cancelled_user_orders_lines.count(),
                       'color': NEGATIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна кількість скасованих найменувань',
                       'uom_ukr': 'шт.'})
    # The total count of units which have been cancelled by the user
    cancelled_user_orders_units_count = cancelled_user_orders_lines.aggregate(
        value=Sum('quantity'))
    statistics.append({'name': 'cancelled_user_orders_units_count',
                       **cancelled_user_orders_units_count,
                       'color': NEGATIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна кількість скасованих одиниць товару',
                       'uom_ukr': 'шт.'})
    # The total price of units which have been cancelled by the user
    cancelled_user_orders_units_amount = cancelled_user_orders_lines.aggregate(
        value=Sum(F('quantity') * F('price')))
    statistics.append({'name': 'cancelled_orders_total',
                       **cancelled_user_orders_units_amount,
                       'color': NEGATIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна вартість скасованих замовлень',
                       'uom_ukr': 'грн'})
    # The total count of lines which have been returned by the user
    returned_user_orders_lines = OrderLine.objects.filter(order__in=returned_orders)
    statistics.append({'name': 'returned_user_orders_lines',
                       'value': returned_user_orders_lines.count(),
                       'color': NEGATIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна кількість повернених найменувань',
                       'uom_ukr': 'шт.'})
    # The total count of units which have been returned by the user
    returned_user_orders_units_count = returned_user_orders_lines.aggregate(
        value=Sum('quantity'))
    statistics.append({'name': 'returned_user_orders_units_count',
                       **returned_user_orders_units_count,
                       'color': NEGATIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна кількість повернених одиниць товару',
                       'uom_ukr': 'шт.'})
    # The total price of units which have been returned by the user
    returned_user_orders_units_amount = returned_user_orders_lines.aggregate(
        value=Sum(F('quantity') * F('price')))
    statistics.append({'name': 'returned_orders_total',
                       **returned_user_orders_units_amount,
                       'color': NEGATIVE_TRANSACTION_COLOR,
                       'title_ukr': 'Загальна вартість повернених замовлень',
                       'uom_ukr': 'грн'})
    return statistics

