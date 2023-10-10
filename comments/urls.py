from django.urls import path
from .views import CommentListAPIView, CommentDeleteUpdateAPIView, \
    CommentCreateAPIView


urlpatterns = [
    path('<int:good_id>/', CommentListAPIView.as_view()),
    path('delete/<str:public_id>/', CommentDeleteUpdateAPIView.as_view()),
    path('create/<str:public_id>/<str:customer>/', CommentCreateAPIView.as_view())
]