from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog import views

app_name = 'blog'

router = DefaultRouter()
router.register('blog', views.BlogViewSet)
router.register('post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
