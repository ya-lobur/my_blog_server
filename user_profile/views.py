import datetime

from django.contrib.auth import get_user_model
from rest_framework import exceptions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.authentication import generate_access_token
from user_profile.serializers import ProfileSerializer

UserModel = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Пароль и его подтверждение не совпадают!')

    serializer = ProfileSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        profile = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        raise exceptions.AuthenticationFailed('Пользователь не найден')
    else:
        if profile.check_password(password):
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            token = generate_access_token(profile, expires=expires)

            response = Response(ProfileSerializer(profile).data)
            response.set_cookie(key='jwt', value=token, expires=expires, httponly=True)

            return response
        else:
            raise exceptions.AuthenticationFailed('Неправильный пароль')


@api_view(['POST'])
def logout(_):
    response = Response()
    response.delete_cookie(key='jwt')
    return response


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user).data)
