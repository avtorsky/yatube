from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from http import HTTPStatus

User = get_user_model()


class UsersURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(
            username='alderson',
            email='alderson@fsociety.com',
            password='mr%r0b0t',
        )

    def test_users_auth_profile_exists(self):
        """Проверяем, что зарегистрированному пользователю создан
        профайл в системе."""
        response = self.guest_client.get(f'/profile/{self.user.username}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_users_profile_nonexists(self):
        """Проверяем, что на запрос несуществующего профайла
        возвращается 404 HTTP-статус."""
        response = self.guest_client.get(f'/profile/{self.user.username}101/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
