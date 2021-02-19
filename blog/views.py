from datetime import date

from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
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
        if isinstance(exc, (Http404, Blog.DoesNotExist)):
            return Response(data={'error': 'Такого блога не существует'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'error': exc.args}, status=exc.status_code if hasattr(exc, 'status_code') else status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

    @action(detail=False, url_path='daily-top-six', pagination_class=None)
    def daily_top_six(self, request):
        top_ten_posts = Post.objects.filter(created__contains=date.today()).order_by('-liked_by__len')[:6]
        serializer = PostModelSerializer(top_ten_posts, many=True)
        return Response({'top_posts': serializer.data})

    @swagger_auto_schema(request_body=no_body)
    @action(methods=['patch'], detail=True, url_path='like')  # TODO: Написать тесты
    def like_post(self, request, pk):
        post: Post = Post.objects.get(pk=pk)
        user_id = request.user.pk

        if user_id in post.liked_by:
            post.liked_by.remove(user_id)
        else:
            post.liked_by.append(user_id)
        post.save()

        return Response(PostModelSerializer(post).data)

    def perform_create(self, serializer):
        if user_blog := self.request.user.blog:
            serializer.save(blog=user_blog, author=self.request.user)

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(data={'error': 'Объект не существует'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'error': exc.args}, status=exc.status_code if hasattr(exc, 'status_code') else status.HTTP_400_BAD_REQUEST)
