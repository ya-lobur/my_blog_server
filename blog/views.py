from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from blog.models import Blog, Post
from blog.serializers import BlogModelSerializer, PostModelSerializer

page_param = openapi.Parameter(
    'page', openapi.IN_QUERY,
    description="A page number within the paginated result set.",
    type=openapi.TYPE_INTEGER
)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer

    @swagger_auto_schema(manual_parameters=[page_param])
    @action(detail=True, url_path='post-list')
    def post_list(self, request, pk):
        posts = Blog.objects.get(pk=pk).posts.all()
        page = self.paginate_queryset(posts)

        if page is not None:
            serializer = PostModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostModelSerializer(posts, many=True)

        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, Blog.DoesNotExist):
            return Response(data={'error': 'Такого блога не существует'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'error': exc.args}, status=exc.status_code if exc.status_code else status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

    def perform_create(self, serializer):
        if user_blog := self.request.user.blog:
            serializer.save(blog=user_blog)

    def handle_exception(self, exc):
        if isinstance(exc, Blog.DoesNotExist):
            return Response(data={'error': 'Такого блога не существует'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'error': exc.args}, status=exc.status_code if exc.status_code else status.HTTP_400_BAD_REQUEST)
