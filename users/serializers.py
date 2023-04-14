from django.contrib.auth import authenticate
from rest_framework import serializers
from .utils import get_admin_tokens_for_user, get_tokens_for_user
from django.conf import settings
from .models import MyUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(required=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        remember_me = data.get('remember_me', False)

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if user.is_active:
                    data['user'] = user

                    if user.is_staff:
                        data['tokens'] = get_admin_tokens_for_user(user)
                    else:
                        data['tokens'] = get_tokens_for_user(user)

                    if remember_me:
                        self.context['request'].session.set_expiry(settings.SESSION_COOKIE_AGE)
                    else:
                        self.context['request'].session.set_expiry(0)

                    return data
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')

        else:
            raise serializers.ValidationError('Must include "email" and "password" fields.')


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
