from django.urls import path
from .views import UserAPIView, UserUpdateAPIView


urlpatterns = [
    path('', UserAPIView.as_view()),
    path('profile/<str:public_id>/', UserUpdateAPIView.as_view()),
]