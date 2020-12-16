from rest_framework import generics

from blog.models import Blog, Post
from blog.serializers import BlogModelSerializer, PostReadUpdateSerializer, PostCreateSerializer


class BlogCreate(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer


class BlogList(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostList(generics.ListAPIView):
    serializer_class = PostReadUpdateSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'blog'):
            return self.request.user.blog.posts.all()
        return Post.objects.none()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostReadUpdateSerializer
