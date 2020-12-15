from django.urls import path, include
from blog import views

urlpatterns = [
    path('list/', views.blog_list),
]
