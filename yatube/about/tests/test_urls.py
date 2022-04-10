from django.test import Client, TestCase

from http import HTTPStatus

AUTHOR_PATH = '/about/author/'
TECH_PATH = '/about/tech/'


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_urls_valid_templates(self):
        """Проверяем, что статический URL-адрес
        использует соответствующий шаблон."""
        templates_url_names = {
            AUTHOR_PATH: 'about/author.html',
            TECH_PATH: 'about/tech.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_about_urls_available_for_unauthorized_users(self):
        """Проверка статических URL-адресов,
        доступных неавторизованным пользователям."""
        url_names = (
            AUTHOR_PATH,
            TECH_PATH,
        )
        for url in url_names:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
