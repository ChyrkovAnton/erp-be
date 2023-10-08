from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'good', 'customer', 'parent', 'text', 'created',
                    'updated', 'active')
