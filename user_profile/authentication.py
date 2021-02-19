import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

UserModel = get_user_model()


def generate_access_token(user: UserModel, expires: datetime.datetime):
    payload = {
        'user_id': user.id,
        'exp': expires,
        'iat': datetime.datetime.utcnow()
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed()

        try:
            user = UserModel.objects.get(id=payload['user_id'])
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('Такого пользователя не существует')
        else:
            return user, token
