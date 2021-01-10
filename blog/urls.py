from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog import views

app_name = 'blog'

router = DefaultRouter()
router.register('blog', views.BlogViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('post-list/', views.PostList.as_view(), name='post-list'),
    path('post-create/', views.PostCreate.as_view(), name='post-create'),
    path('post-detail/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
]
