from django.urls import path

from user_profile.views import register, login, ProfileAPIView

app_name = 'user_profile'


urlpatterns = [
    path('register', register),
    path('login', login),
    path('info', ProfileAPIView.as_view()),

]
