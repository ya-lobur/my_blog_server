from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Blog, Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class PostModelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для операций чтения и обновления
    """
    blog_id = serializers.PrimaryKeyRelatedField(read_only=True)
    liked_by = serializers.ListField(read_only=True)
    author = AuthorSerializer(read_only=True)

    # def get_author(self, obj):
    #     return AuthorSerializer(obj.author).data

    class Meta:
        model = Post
        exclude = ('created', 'updated', 'blog')


class BlogModelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для операций чтения/обновления/создания
    """
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Blog
        exclude = ('created', 'updated', 'owner')
