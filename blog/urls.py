from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('blog-list/', views.BlogList.as_view()),
    path('blog-create/', views.BlogCreate.as_view(), name='blog-create'),
    path('blog-detail/<int:pk>/', views.BlogDetail.as_view(), name='blog-detail'),
    path('post-list/', views.PostList.as_view(), name='post-list'),
    path('post-create/', views.PostCreate.as_view(), name='post-create'),
    path('post-detail/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
]
