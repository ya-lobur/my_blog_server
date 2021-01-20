from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.index),
    path('<path:url>', views.index)
]