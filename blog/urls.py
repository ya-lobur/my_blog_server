from django.urls import path, include
from blog import views

urlpatterns = [
    path('blog-list/', views.BlogList.as_view()),
    path('blog-create/', views.BlogCreate.as_view()),
    path('blog-detail/<int:pk>/', views.BlogDetail.as_view()),
    path('post-list/', views.PostList.as_view()),
    path('post-create/', views.PostCreate.as_view()),
    path('post-detail/<int:pk>/', views.PostDetail.as_view()),
]
