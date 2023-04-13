from django.urls import path
from .views import MyRegistrationView, MyLogoutView, MyChangePasswordView, login, MyLoginView
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'


urlpatterns = [
    path('accounts/login/', MyLoginView.as_view(), name='login'),
    path('accounts/register/', MyRegistrationView.as_view(), name='register'),
    path('accounts/logout', MyLogoutView.as_view(), name='logout'),
    path('accounts/change-password', MyChangePasswordView.as_view(), name='change_password'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

