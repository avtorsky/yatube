from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from http import HTTPStatus

from ..models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='elliot')
        cls.group = Group.objects.create(
            title='Мистер робот',
            slug='mr-robot',
            description='Сделать мир лучше',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Привет, друг',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_posts_urls_valid_templates(self):
        """Проверяем, что URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_posts_urls_available_for_unauthorized_users(self):
        """Проверка URL-адресов, доступных неавторизованным пользователям."""
        url_names = (
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user.username}/',
            f'/posts/{self.post.pk}/',
        )
        for url in url_names:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_create_url_available_for_authorized_users(self):
        """Проверяем, что URL-адрес /create/ доступен только авторизованным
        пользователям."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_edit_url_available_for_authorized_author(self):
        """Проверяем, что URL-адрес /posts/{id}/edit/ доступен только
        авторизованному автору."""
        response = self.authorized_client.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_redirect_url_for_unauthorized_users(self):
        """Проверяем отработку редиректов при запросе URL-адресов, доступных
        только авторизованным пользователям."""
        url_names = (
            '/create/',
            f'/posts/{self.post.pk}/edit/',
        )
        for url in url_names:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
                self.assertRedirects(response, f'/auth/login/?next={url}')

    def test_posts_page_not_found(self):
        """Проверяем, что запрос несуществующего URL-адреса возвращает
        404 HTTP-статус."""
        response = self.guest_client.get('/fsociety404/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
