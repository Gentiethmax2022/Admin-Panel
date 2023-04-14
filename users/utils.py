from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

def get_admin_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    # Add admin claims to the access token
    access_token['is_admin'] = True

    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }
    

