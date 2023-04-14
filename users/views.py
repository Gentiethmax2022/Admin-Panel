from django.contrib.auth import authenticate, login, logout   #type: ignore
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from .utils import get_tokens_for_user, get_admin_tokens_for_user
from .serializers import LoginSerializer, RegistrationSerializer

from .forms import PasswordChangeForm
from .models import MyUser


class MyRegistrationView(APIView, TemplateView):
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'registration.html', {'errors': serializer.errors})


from rest_framework.authtoken.models import Token
from django.contrib.admin.views.decorators import staff_member_required
class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        if user.is_staff:
            auth_data = get_admin_tokens_for_user(user)
        else:
            auth_data = get_tokens_for_user(user)

        remember_me = serializer.validated_data.get('remember_me', False)

        if remember_me:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)

        return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)

class MyLoginView(LoginView, TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
    def post(self, request, *args, **kwargs):
        return LoginView.as_view()(request._request)

# Only admins can access the MyLoginView
staff_member_required(MyLoginView.as_view())




# from django.contrib.admin.views.decorators import staff_member_required

# class LoginView(APIView):
#     def post(self, request):
#         print(request.POST)
#         print(request.data)
#         if 'email' not in request.data or 'password' not in request.data:
#             return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        
#         email = request.data['email']
#         password = request.data['password']
#         print(email, password)
#         print(request.data)
#         # check if user with provided email exists
#         user = MyUser.objects.filter(email=email).first()
#         print(user)
#         if user is None:
#             return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
#         # Authenticate the user with the provided password
#         user = authenticate(request, email=email, password=password)
        
#         if user is not None:
#             login(request, user) #type: ignore
#             if user.is_staff:    #type: ignore
#                 # if user is an admin, generate admin tokens
#                 auth_data = get_admin_tokens_for_user(request.user)
#             else:
#                 # if user is not an admin, generate regular user tokens
#                 auth_data = get_tokens_for_user(request.user)

#             # Set session expiry time based on "remember_me" parameter
#             remember_me = request.data.get('remember_me', False)
#             if remember_me:
#                 request.session.set_expiry(settings.SESSION_COOKIE_AGE) #type: ignore
#             else:
#                 request.session.set_expiry(0)

#             return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
#         return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class MyLoginView(LoginView, TemplateView):
#     template_name = 'login.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})
    
#     def post(self, request, *args, **kwargs):
#         return LoginView.as_view()(request._request)

# # Only admins can access the MyLoginView
# staff_member_required(MyLoginView.as_view())



class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class MyLogoutView(LogoutView, TemplateView):
    template_name = 'logout.html'


# class ChangePasswordView(APIView):
#     permission_classes = [IsAuthenticated, ]

#     def post(self, request):
#         serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
#         serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
#         request.user.set_password(serializer.validated_data['new_password'])  #type: ignore
#         request.user.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class MyChangePasswordView(ChangePasswordView, TemplateView):
#     template_name = 'change_password.html'


class MyChangePasswordView(TemplateView):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()  #type: ignore
            update_session_auth_hash(request, form.user)   #type: ignore
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
            return self.render_to_response({'form': form})

