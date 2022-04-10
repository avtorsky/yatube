from django.test import TestCase, Client

from http import HTTPStatus

from ..models import Group, Post, User

INDEX_PATH = '/'
POST_CREATE_PATH = '/create/'
NOT_FOUND_PATH = '/fsociety404/'


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
        cls.GROUP_PATH = f'/group/{cls.group.slug}/'
        cls.PROFILE_PATH = f'/profile/{cls.user.username}/'
        cls.POST_DETAIL_PATH = f'/posts/{cls.post.pk}/'
        cls.POST_EDIT_PATH = f'/posts/{cls.post.pk}/edit/'

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_posts_urls_valid_templates(self):
        """Проверяем, что URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            INDEX_PATH: 'posts/index.html',
            self.GROUP_PATH: 'posts/group_list.html',
            self.PROFILE_PATH: 'posts/profile.html',
            self.POST_DETAIL_PATH: 'posts/post_detail.html',
            POST_CREATE_PATH: 'posts/create_post.html',
            self.POST_EDIT_PATH: 'posts/create_post.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_posts_urls_available_for_unauthorized_users(self):
        """Проверка URL-адресов, доступных неавторизованным пользователям."""
        url_names = (
            INDEX_PATH,
            self.GROUP_PATH,
            self.PROFILE_PATH,
            self.POST_DETAIL_PATH,
        )
        for url in url_names:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_create_url_available_for_authorized_users(self):
        """Проверяем, что URL-адрес /create/ доступен только авторизованным
        пользователям."""
        response = self.authorized_client.get(POST_CREATE_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_edit_url_available_for_authorized_author(self):
        """Проверяем, что URL-адрес /posts/{id}/edit/ доступен только
        авторизованному автору."""
        response = self.authorized_client.get(self.POST_EDIT_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_redirect_url_for_unauthorized_users(self):
        """Проверяем отработку редиректов при запросе URL-адресов, доступных
        только авторизованным пользователям."""
        url_names = (
            POST_CREATE_PATH,
            self.POST_EDIT_PATH,
        )
        for url in url_names:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
                self.assertRedirects(response, f'/auth/login/?next={url}')

    def test_posts_page_not_found(self):
        """Проверяем, что запрос несуществующего URL-адреса возвращает
        404 HTTP-статус."""
        response = self.guest_client.get(NOT_FOUND_PATH)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
