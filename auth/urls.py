from django.urls import path
from auth.viewsets.register import RegisterViewSet
from auth.viewsets.login import LoginViewSet
from auth.viewsets.refresh import RefreshViewSet

AUTH_ACTION = {'post': 'create'}
urlpatterns = [
    path('register/', RegisterViewSet.as_view(AUTH_ACTION)),
    path('login/', LoginViewSet.as_view(AUTH_ACTION)),
    path('refresh/', RefreshViewSet.as_view(AUTH_ACTION)),
]