from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import  LoginView, RegisterView, UserView
urlpatterns = [
    path('api/users/', UserView.as_view(), name='users'),
    path('api/register/', RegisterView.as_view(), name='register'), 
    path('api/login/', LoginView.as_view(), name='login'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('auth/', include('social_django.urls', namespace='social')),
  
]
