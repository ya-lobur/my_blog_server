from django.urls import path

from user_profile.views import register, verify, login, logout, ProfileAPIView

app_name = 'user_profile'

urlpatterns = [
    path('register', register, name='register'),
    path('verify/<uuid:uuid>', verify, name='verify'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('info', ProfileAPIView.as_view()),
]
