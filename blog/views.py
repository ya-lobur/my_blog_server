from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from blog.models import Blog, Post
from blog.serializers import BlogModelSerializer, PostModelSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer


# Думаю стоит воткнуть action для Blog, который бы отдавал список постов этого блога
# class PostList(generics.ListAPIView):
#     serializer_class = PostModelSerializer
#
#     def get_queryset(self):
#         blog_id = self.request.query_params.get('blog', None)
#
#         if blog_id is None and self.request.user.is_authenticated:
#             blog_id = self.request.user.blog.pk
#
#         if blog_id:
#             return Post.objects.filter(blog_id=blog_id)
#         return Post.objects.none()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

    def perform_create(self, serializer):
        if user_blog := self.request.user.blog:
            serializer.save(blog=user_blog)

    def handle_exception(self, exc):
        """На случай, если нет блога"""
        if isinstance(exc, ObjectDoesNotExist):
            return Response(data={'error': exc.args}, status=status.HTTP_404_NOT_FOUND)
