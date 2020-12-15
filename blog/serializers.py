from rest_framework import serializers
from blog.models import Blog, Post


class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('created', 'updated')


class BlogModelSerializer(serializers.ModelSerializer):
    posts = PostModelSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'description', 'posts')
