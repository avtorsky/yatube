from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from http import HTTPStatus

User = get_user_model()


class UsersFormTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_users_form_creates_new_user_entry_in_db(self):
        """Проверяем, что при заполнении формы создаётся новый пользователь."""
        users_db_count = User.objects.count()
        form_data = {
            'username': 'alderson',
            'password1': 'mr%r0b0t',
            'password2': 'mr%r0b0t',
        }
        response = self.guest_client.post(
            reverse('users:signup'), data=form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.count(), users_db_count + 1)
        self.assertTrue(
            User.objects.filter(
                username='alderson',
            ).exists()
        )
        self.assertRedirects(response, reverse('posts:index'))
