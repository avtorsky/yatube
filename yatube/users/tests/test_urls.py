from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UsersURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(
            username='alderson',
            email='alderson@fsociety.com',
            password='mr%r0b0t',
        )
        self.TARGET_PROFILE_PATH = f'/profile/{self.user.username}/'
        self.YET_ANOTHER_PROFILE_PATH = f'/profile/{self.user.username}101/'

    def test_users_auth_profile_exists(self):
        """Проверяем, что зарегистрированному пользователю создан
        профайл в системе."""
        response = self.guest_client.get(self.TARGET_PROFILE_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_users_profile_nonexists(self):
        """Проверяем, что на запрос несуществующего профайла
        возвращается 404 HTTP-статус."""
        response = self.guest_client.get(self.YET_ANOTHER_PROFILE_PATH)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
