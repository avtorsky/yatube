from django.test import TestCase, Client
from django.urls import reverse

from http import HTTPStatus


class AboutViewTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_views_valid_templates(self):
        """Проверяем, что статические views используют
        соответствующий шаблон."""
        namespace_names = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for name, template in namespace_names.items():
            with self.subTest(name=name):
                response = self.guest_client.get(name)
                self.assertTemplateUsed(response, template)

    def test_about_views_available_for_unauthorized_users(self):
        """Проверяем, что статические views доступны
        неавторизованным пользователям."""
        namespace_names = (
            reverse('about:author'),
            reverse('about:tech'),
        )
        for name in namespace_names:
            with self.subTest():
                response = self.guest_client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)
