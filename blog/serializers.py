from rest_framework import serializers
from blog.models import Blog, Post


class PostModelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для операций чтения и обновления
    """
    blog_id = serializers.PrimaryKeyRelatedField(read_only=True)

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
