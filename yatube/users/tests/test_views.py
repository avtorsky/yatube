from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()

USER_CREATE_VIEW = reverse('users:signup')
USER_LOGIN_VIEW = reverse('users:login')
USER_LOGOUT_VIEW = reverse('users:logout')
USER_PASSWORD_RESET_VIEW = reverse('users:password_reset')
USER_PASSWORD_RESET_DONE_VIEW = reverse('users:password_reset_done')
USER_PASSWORD_RESET_FIN_VIEW = reverse('users:password_reset_complete')


class UsersViewTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_users_views_valid_templates(self):
        """Проверяем, что views используют соответствующий шаблон."""
        namespace_names = {
            USER_CREATE_VIEW: 'users/signup.html',
            USER_LOGIN_VIEW: 'users/login.html',
            USER_LOGOUT_VIEW: 'users/logged_out.html',
            USER_PASSWORD_RESET_VIEW: 'users/password_reset_form.html',
            USER_PASSWORD_RESET_DONE_VIEW: 'users/password_reset_done.html',
            USER_PASSWORD_RESET_FIN_VIEW: 'users/password_reset_complete.html',
        }
        for name, template in namespace_names.items():
            with self.subTest(name=name):
                response = self.guest_client.get(name)
                self.assertTemplateUsed(response, template)

    def test_users_signup_page_valid_context(self):
        """Проверяем, что во view страницы регистрации пользователя
        отрисована форма с правильным context."""

        response = self.guest_client.get(USER_CREATE_VIEW)
        self.assertIsInstance(
            response.context['form'].fields['username'],
            forms.fields.CharField,
        )
        self.assertIsInstance(
            response.context['form'].fields['email'],
            forms.fields.EmailField,
        )
