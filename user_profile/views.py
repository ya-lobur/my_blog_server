import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import exceptions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog
from user_profile.authentication import generate_access_token
from user_profile.serializers import ProfileSerializer

ProfileModel = get_user_model()


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


@api_view(['GET'])
@permission_classes([AllowAny])
def verify(request, uuid):
    try:
        profile = ProfileModel.objects.get(verification_uuid=uuid, is_verified=False)
    except ProfileModel.DoesNotExist:
        raise exceptions.NotFound("Profile does not exist or is already verified")

    profile.is_verified = True
    profile.save()

    # Verified profile gets full functionality (gets a blog)
    Blog.objects.create(owner=profile)

    return redirect('http://localhost:8000/login?verified=1')


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        profile = ProfileModel.objects.get(email=email)
    except ProfileModel.DoesNotExist:
        raise exceptions.AuthenticationFailed('Пользователь не найден')
    else:
        if profile.is_verified and profile.check_password(password):
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            token = generate_access_token(profile, expires=expires)

            response = Response(ProfileSerializer(profile).data)
            response.set_cookie(key='jwt', value=token, expires=expires, httponly=True)

            return response
        else:
            raise exceptions.AuthenticationFailed('Введен неправильный пароль или пользователь не верифицирован')


@api_view(['POST'])
def logout(_):
    response = Response()
    response.delete_cookie(key='jwt')
    return response


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user).data)
