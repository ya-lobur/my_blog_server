from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status

from blog.models import Blog, Post
from blog.serializers import BlogModelSerializer, PostModelSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

    def perform_create(self, serializer):
        if user_blog := self.request.user.blog:
            serializer.save(blog=user_blog)

    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return Response(data={'error': exc.args}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostList(generics.ListAPIView):
    serializer_class = PostModelSerializer

    def get_queryset(self):
        blog_id = self.request.query_params.get('blog', None)

        if blog_id is None and self.request.user.is_authenticated:
            blog_id = self.request.user.blog.pk

        if blog_id:
            return Post.objects.filter(blog_id=blog_id)
        return Post.objects.none()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
