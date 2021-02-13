from django.urls import path
from rest_framework.authtoken import views

from user_profile.views import register, ProfileAPIView

app_name = 'user_profile'


urlpatterns = [
    path('register', register),
    path('login', views.obtain_auth_token),
    path('info', ProfileAPIView.as_view()),

]
