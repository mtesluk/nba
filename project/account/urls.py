from django.urls import path, include
from .views import UserView


urlpatterns = [
    path('auth-user', UserView.as_view()),
]
