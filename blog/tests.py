import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Blog, Post
from blog.serializers import BlogModelSerializer, PostModelSerializer


def create_user(name: str) -> User:
    return User.objects.create_user(username=name, password=name, email=f'{name}@test.ru')


class BlogTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = create_user('user1')
        cls.blog = Blog.objects.create(owner=cls.user1, description='some description')

    def setUp(self) -> None:
        self.client.force_login(self.user1)

    def test_blog_detail_read(self):
        """Должен отдать информацию о блоге"""

        url = reverse('blog:blog-detail', args=[self.user1.blog.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, BlogModelSerializer(self.user1.blog).data)

    def test_blog_detail_patch(self):
        """Должен обновить информацию о блоге"""

        url = reverse('blog:blog-detail', args=[self.user1.blog.pk])
        new_description = 'updated description'
        response = self.client.patch(url, data=json.dumps({'description': new_description}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, BlogModelSerializer(Blog.objects.get(pk=self.user1.blog.pk)).data)
        self.assertEqual(response.data['description'], new_description)

    def test_post_list_action(self):
        """Должен вернуть пагинированный список постов блога"""

        post = Post.objects.create(blog=self.blog, text_content='Some content')
        url = reverse('blog:blog-post-list', args=[self.blog.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'count': 1, 'next': None, 'previous': None, 'results': [PostModelSerializer(post).data]})



class PostTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = create_user('user1')
        cls.blog = Blog.objects.create(owner=cls.user1, description='some description')

    def setUp(self) -> None:
        self.client.force_login(self.user1)

    def test_post_detail_read(self):
        """Должен возвращать пост"""
        post = Post.objects.create(blog=self.user1.blog, text_content='some interesting content')

        url = reverse('blog:post-detail', args=[post.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, PostModelSerializer(post).data)

    def test_post_list_without_blog_param(self):
        """Должен отдавать список постов текущего юзера"""
        post_1 = Post.objects.create(blog=self.user1.blog, text_content='some interesting content')
        post_2 = Post.objects.create(blog=self.user1.blog, text_content='just content')

        url = reverse('blog:post-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.data['results'], PostModelSerializer([post_1, post_2], many=True).data)

    def test_post_list_with_blog_param(self):
        """Должен отдавать список постов блога, id которого указан в параметре blog"""
        user2 = create_user('user2')
        user2_blog: Blog = Blog.objects.create(owner=user2)
        post_1 = Post.objects.create(blog=user2_blog, text_content='some interesting content')
        post_2 = Post.objects.create(blog=user2_blog, text_content='just content')

        url = f"{reverse('blog:post-list')}?blog={user2_blog.pk}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.data['results'], PostModelSerializer([post_1, post_2], many=True).data)

    def test_simple_post_create(self):
        """Должен создавать пост"""
        # Хз почему Django по дефолту дает post-у на создание name как post-list. Видимо т.к. они detail==False:
        url = reverse('blog:post-list')

        data = {'text_content': 'content'}

        response = self.client.post(path=url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, PostModelSerializer(Post.objects.get(pk=response.data['id'])).data)

    def test_post_detail_patch(self):
        """Должен обновить только text_content"""
        post = Post.objects.create(blog=self.blog, text_content='old content')

        url = reverse('blog:post-detail', args=[post.pk])
        new_data = {'text_content': 'new interesting text'}
        response = self.client.patch(path=url, data=json.dumps(new_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['text_content'], new_data['text_content'])
        self.assertDictEqual(response.data, PostModelSerializer(Post.objects.get(pk=post.pk)).data)

    def test_post_detail_delete(self):
        """Должен удалить пост"""
        post = Post.objects.create(blog=self.blog, text_content='old content')

        url = reverse('blog:post-detail', args=[post.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertQuerysetEqual(Post.objects.none(), Post.objects.filter(pk=post.pk))
