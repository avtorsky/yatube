from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

AUTHOR_VIEW = reverse('about:author')
TECH_VIEW = reverse('about:tech')


class AboutViewTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_views_valid_templates(self):
        """Проверяем, что статические views используют
        соответствующий шаблон."""
        namespace_names = {
            AUTHOR_VIEW: 'about/author.html',
            TECH_VIEW: 'about/tech.html',
        }
        for name, template in namespace_names.items():
            with self.subTest(name=name):
                response = self.guest_client.get(name)
                self.assertTemplateUsed(response, template)

    def test_about_views_available_for_unauthorized_users(self):
        """Проверяем, что статические views доступны
        неавторизованным пользователям."""
        namespace_names = (
            AUTHOR_VIEW,
            TECH_VIEW,
        )
        for name in namespace_names:
            with self.subTest():
                response = self.guest_client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)
