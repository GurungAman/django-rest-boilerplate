from multiprocessing import AuthenticationError
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header, BaseAuthentication
import jwt

User = get_user_model()


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(' ')
        if auth_header == b'':
            raise AuthenticationFailed('No token provided.')
        if len(auth_token) != 2:
            raise AuthenticationFailed('Bad authorization header.')
        try:
            token = auth_token[1]
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            email = payload['email']

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                'Token has expired.')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token.')

        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed('User not found.')
        if not user.is_active:
            raise AuthenticationFailed('User is not active.')
        return (user, token)
