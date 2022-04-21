from http import HTTPStatus

from django.test import Client, TestCase, override_settings
from django.views.defaults import page_not_found

NOT_FOUND_VIEW = page_not_found
NOT_FOUND_TEMPLATE = 'core/404.html'


@override_settings(DEBUG=False)
class CoreViewTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_core_error_view_valid_template(self):
        """Проверяем, что view страницы с ошибкой
        использует соответствующий шаблон."""
        template_config = {
            NOT_FOUND_VIEW: NOT_FOUND_TEMPLATE,
        }
        for view, template in template_config.items():
            with self.subTest(view=view):
                response = self.guest_client.get(view)
                self.assertTemplateUsed(response, template)

    def test_core_error_view_valid_status(self):
        """Проверяем, что view страницы с ошибкой отрисована
        в ответ на соответствующий HTTP-статус."""
        status_config = {
            NOT_FOUND_VIEW: HTTPStatus.NOT_FOUND,
        }
        for view, status in status_config.items():
            with self.subTest(view=view):
                response = self.guest_client.get(view)
                self.assertEqual(response.status_code, status)
