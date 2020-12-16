from rest_framework import serializers
from blog.models import Blog, Post


class PostReadUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для операций чтения и обновления
    """
    blog_id = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), required=False)

    class Meta:
        model = Post
        exclude = ('created', 'updated', 'blog')


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания поста
    """
    blog_id = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())

    class Meta:
        model = Post
        exclude = ('created', 'updated', 'blog')


class BlogModelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для операций чтения/обновления/создания
    """
    # posts = PostModelSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        exclude = ('created', 'updated',)
