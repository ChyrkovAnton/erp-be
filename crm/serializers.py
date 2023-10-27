from rest_framework import serializers
from .models import OrderStatus, Order, StatusChange, OrderLine, PostCompany, \
                    PostOffice, OrderDestination
from user.models import User


class OrderStatusSerializer (serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = OrderStatus
        fields = ['id', 'status_name', 'description', 'is_active']


class OrderLineSerializer (serializers.ModelSerializer):

    class Meta:
        model = OrderLine
        fields = ['id', 'order', 'good', 'quantity', 'price']
        extra_kwargs = {'order': {'required': False}}


class OrderSerializer (serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    order_lines = OrderLineSerializer(source='order_line_order', many=True)
    customer = serializers.UUIDField(source='customer.public_id', read_only=True, format='hex')

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_number', 'order_place_point',
                  'discount', 'additional_information', 'customer_first_name',
                  'customer_middle_name', 'customer_last_name',
                  'customer_phone', 'customer_email', 'order_destination',
                  'order_lines', 'carrier', 'payment_type']


class OrderSerializerCreate(OrderSerializer):
    order_lines = OrderLineSerializer(many=True)

    def create(self, validated_data):
        customer = self.context['request'].data['customer']
        user = User.objects.get(public_id=customer)
        lines = validated_data.pop('order_lines')
        order = Order.objects.create(**validated_data)
        order.customer = user
        order.save()
        for line in lines:
            OrderLine.objects.create(order=order, **line)
        order.order_lines = list(order.order_line_order.all())
        return order


class CitiesPostOfficeSerializer (serializers.ModelSerializer):

    class Meta:
        model = PostOffice
        fields = ['city_description']
