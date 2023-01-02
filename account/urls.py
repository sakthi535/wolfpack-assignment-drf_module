from django.contrib import admin
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, ImageGeneratorView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name = 'registration'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('profile/', UserProfileView.as_view(), name = 'profile'),
    path('image/', ImageGeneratorView.as_view(), name = 'image')
]
