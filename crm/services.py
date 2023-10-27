from django.db.models import Sum, F
from user.models import User
from crm.models import OrderLine


def get_customer_statistics(request, **kwargs):
    statistics = []
    user = User.objects.get(public_id=kwargs['user'])
    # The total count of orders which have been ordered by the user
    user_orders = user.orders.all()
    statistics.append({'order_number': user_orders.count()})
    # The total count of orders which have been paid by the user
    paid_orders = user_orders.filter(is_paid=True)
    success_ord_count = {'successful_order_number': paid_orders.count()}
    statistics.append(success_ord_count)
    # The total count of orders which have been returned by the user
    returned_orders = user_orders.filter(is_returned=True)
    ret_ord_count = {'returned_order_number': returned_orders.count()}
    statistics.append(ret_ord_count)
    # The total count of orders which have been cancelled by the user
    cancelled_orders = user_orders.filter(is_cancelled=True)
    cnld_ord_count = {'cancelled_order_number': cancelled_orders.count()}
    statistics.append(cnld_ord_count)
    # The total count of lines which have been ordered by the user
    user_orders_lines = OrderLine.objects.filter(order__in=user_orders)
    statistics.append({'order_lines_count': user_orders_lines.count()})
    # The total count of units which have been ordered by the user
    user_orders_units_count = user_orders_lines.aggregate(
        user_orders_units_count=Sum('quantity'))
    statistics.append(user_orders_units_count)
    # The total price of units which have been ordered by the user
    user_orders_units_amount = user_orders_lines.aggregate(
        orders_total=Sum(F('quantity') * F('price')))
    statistics.append(user_orders_units_amount)
    # The total count of lines which have been paid by the user
    paid_user_orders_lines = OrderLine.objects.filter(order__in=paid_orders)
    statistics.append({'paid_user_orders_lines': paid_user_orders_lines.count()})
    # The total count of units which have been paid by the user
    paid_user_orders_units_count = paid_user_orders_lines.aggregate(
        paid_user_orders_units_count=Sum('quantity'))
    statistics.append(paid_user_orders_units_count)
    # The total price of units which have been paid by the user
    paid_user_orders_units_amount = paid_user_orders_lines.aggregate(
        paid_orders_total=Sum(F('quantity') * F('price')))
    statistics.append(paid_user_orders_units_amount)
    return statistics

