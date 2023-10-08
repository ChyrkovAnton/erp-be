from rest_framework import serializers
from .models import Comment


class CommentSerializer (serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'parent', 'good', 'customer', 'customer_name', 'text', 'created']

