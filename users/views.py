from django.contrib.auth import authenticate, login, logout   #type: ignore
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer #type: ignore

from .forms import PasswordChangeForm
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
#     def post(self, request):
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             messages.success(request, 'User successfully created. Click <a href="{}">here</a> to log in.'.format(reverse('login')))
#             return redirect('login')  # Change 'login' to the name of your login URL pattern
#         if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return render(request, 'registration.html', {'errors': serializer.errors})


class LoginView(APIView):
    def post(self, request):
        print(request.data)
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user) #type: ignore
            auth_data = get_tokens_for_user(request.user)

            # Set session expiry time based on "remember_me" parameter
            remember_me = request.data.get('remember_me', False)
            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE) #type: ignore
            else:
                request.session.set_expiry(0)

            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class MyLoginView(LoginView, TemplateView):
    template_name = 'login.html'


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

