from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from my_blog_server import settings

schema_view = get_schema_view(
    openapi.Info(title="Blog Server API", default_version='v1', ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('profile/', include('user_profile.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Урлы фронта должны быть в самом конце
urlpatterns.append(path('', include('frontend.urls')))
