from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from user_profile.serializers import ProfileSerializer

UserModel = get_user_model()


def create_profile(name: str, **kwargs) -> UserModel:
    user = UserModel.objects.create_user(email=f'{name}@test.ru', **kwargs)

    if password := kwargs.get('password'):
        user.set_password(password)
        user.save()

    return user


def login(client, email, password):
    url = reverse('user_profile:login')
    client.post(url, {'email': email, 'password': password})


class ProfileTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.existing_user = create_profile('existing_user', password='1234')

    def test_registration_with_valid_data(self):
        """Должен создать Profile в бд с указанными данными"""

        registration_data = {
            'email': 'ivan@test.ru',
            'password': '1234', 'password_confirm': '1234',
            'first_name': 'Иван', 'last_name': 'Иванов'
        }

        url = reverse('user_profile:register')
        response = self.client.post(url, registration_data)

        created_profile = UserModel.objects.get(email=registration_data['email'])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(registration_data['email'], created_profile.email)
        self.assertEqual(registration_data['first_name'], created_profile.first_name)
        self.assertEqual(registration_data['last_name'], created_profile.last_name)

    def test_login_with_valid_data(self):
        """Должен авторизоваться и вернуть данные авторизованного профиля"""

        login_data = {'email': self.existing_user.email, 'password': '1234'}
        url = reverse('user_profile:login')
        response = self.client.post(url, login_data)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, ProfileSerializer(self.existing_user).data)
