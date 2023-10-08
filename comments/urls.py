from django.urls import path
from .views import CommentAPIView, CommentDeleteUpdateAPIView


urlpatterns = [
    path('<int:good_id>/', CommentAPIView.as_view()),
    path('delete/<int:pk>/', CommentDeleteUpdateAPIView.as_view())
]