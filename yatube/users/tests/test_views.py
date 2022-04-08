from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

User = get_user_model()


class UsersViewTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_users_views_valid_templates(self):
        """Проверяем, что views используют соответствующий шаблон."""
        namespace_names = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:logout'): 'users/logged_out.html',
            reverse('users:password_reset'): 'users/password_reset_form.html',
            reverse(
                'users:password_reset_done'
            ): 'users/password_reset_done.html',
            reverse(
                'users:password_reset_complete'
            ): 'users/password_reset_complete.html',
        }
        for name, template in namespace_names.items():
            with self.subTest(name=name):
                response = self.guest_client.get(name)
                self.assertTemplateUsed(response, template)

    def test_users_signup_page_valid_context(self):
        """Проверяем, что во view страницы регистрации пользователя
        отрисована форма с правильным context."""

        response = self.guest_client.get(reverse('users:signup'))
        self.assertIsInstance(
            response.context['form'].fields['username'],
            forms.fields.CharField,
        )
        self.assertIsInstance(
            response.context['form'].fields['email'],
            forms.fields.EmailField,
        )
