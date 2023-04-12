from django.urls import path
from .views import RegistrationView, LoginView, LogoutView,ChangePasswordView, login_view
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='change_password'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

