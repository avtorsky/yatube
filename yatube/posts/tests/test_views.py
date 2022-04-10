from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from ..models import Group, Post, User

INDEX_VIEW = reverse('posts:index')
POST_CREATE_VIEW = reverse('posts:post_create')
OBJECTS_PER_PAGE = settings.PAGINATOR_SLICING_CONFIG


class PostsViewTests(TestCase):
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
            group=cls.group,
        )
        cls.GROUP_VIEW = reverse(
            'posts:group_list', kwargs={'slug': cls.group.slug}
        )
        cls.PROFILE_VIEW = reverse(
            'posts:profile', kwargs={'username': cls.user.username}
        )
        cls.POST_DETAIL_VIEW = reverse(
            'posts:post_detail', kwargs={'post_id': cls.post.pk}
        )
        cls.POST_EDIT_VIEW = reverse(
            'posts:post_edit', kwargs={'post_id': cls.post.pk}
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def context_validation_config(self, context):
        with self.subTest(context=context):
            self.assertEqual(context.text, self.post.text)
            self.assertEqual(context.pub_date, self.post.pub_date)
            self.assertEqual(context.author, self.post.author)
            self.assertEqual(context.group.pk, self.post.group.pk)

    def test_posts_views_valid_templates(self):
        """Проверяем, что views используют соответствующий шаблон."""
        namespace_names = {
            INDEX_VIEW: 'posts/index.html',
            self.GROUP_VIEW: 'posts/group_list.html',
            self.PROFILE_VIEW: 'posts/profile.html',
            self.POST_DETAIL_VIEW: 'posts/post_detail.html',
            POST_CREATE_VIEW: 'posts/create_post.html',
            self.POST_EDIT_VIEW: 'posts/create_post.html',
        }
        for name, template in namespace_names.items():
            with self.subTest(name=name):
                response = self.authorized_client.get(name)
                self.assertTemplateUsed(response, template)

    def test_posts_index_page_valid_context(self):
        """Проверяем, что во view элемента главной страницы отрисован
        правильный context."""
        response = self.guest_client.get(INDEX_VIEW)
        self.context_validation_config(response.context['page_obj'][0])

    def test_posts_group_page_valid_context(self):
        """Проверяем, что во view элемента страницы группы отрисован
        правильный context."""
        response = self.guest_client.get(self.GROUP_VIEW)
        self.assertEqual(response.context['group'], self.group)
        self.context_validation_config(response.context['page_obj'][0])

    def test_posts_profile_page_valid_context(self):
        """Проверяем, что во view элемента страницы профиля отрисован
        правильный context."""
        response = self.guest_client.get(self.PROFILE_VIEW)
        self.assertEqual(response.context['author'], self.user)
        self.context_validation_config(response.context['page_obj'][0])

    def test_posts_post_page_valid_context(self):
        """Проверяем, что во view страницы просмотра сообщения отрисован
        правильный context."""
        response = self.guest_client.get(self.POST_DETAIL_VIEW)
        self.context_validation_config(response.context['post'])

    def test_posts_create_edit_page_valid_context(self):
        """Проверяем, что во view страницы создания/редактирования сообщения
        отрисована форма с правильным context."""
        context_config = (
            POST_CREATE_VIEW,
            self.POST_EDIT_VIEW,
        )
        for item in context_config:
            with self.subTest(item=item):
                response = self.authorized_client.get(item)
                self.assertIsInstance(
                    response.context['form'].fields['text'],
                    forms.fields.CharField,
                )
                self.assertIsInstance(
                    response.context['form'].fields['group'],
                    forms.fields.ChoiceField,
                )


class PostsAttributionTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='elliot')
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.bot = User.objects.create_user(username='mr_robot')
        self.bot_client = Client()
        self.bot_client.force_login(self.bot)

        self.author_group = Group.objects.create(
            title='Эллиот говорит',
            slug='elliot',
            description='Сделать мир лучше',
        )

        self.bot_group = Group.objects.create(
            title='Робот говорит',
            slug='mr-robot',
            description='Сделать мир хуже',
        )

        self.post = Post.objects.create(
            author=self.author,
            text='Привет, друг',
            group=self.author_group,
        )

        self.TARGET_GROUP_VIEW = reverse(
            'posts:group_list', kwargs={'slug': self.author_group.slug}
        )
        self.YET_ANOTHER_GROUP_VIEW = reverse(
            'posts:group_list', kwargs={'slug': self.bot_group.slug}
        )
        self.TARGET_PROFILE_VIEW = reverse(
            'posts:profile', kwargs={'username': self.author.username}
        )

    def test_posts_new_post_renders_at_relevant_page(self):
        """Проверяем, что во views главной страницы, страницы группы
        и профиле автора отрисовано новое сообщение автора
        с правильным context."""
        views_config = (
            INDEX_VIEW,
            self.TARGET_GROUP_VIEW,
            self.TARGET_PROFILE_VIEW,
        )
        for view in views_config:
            with self.subTest(view=view):
                response = self.author_client.get(view)
                self.assertEqual(response.context['page_obj'][0], self.post)

    def test_posts_new_post_no_render_at_irrelevant_page(self):
        """Проверяем, что во view страницы нецелевой группы новое целевое
        сообщение автора не отрисовано."""
        view = self.YET_ANOTHER_GROUP_VIEW
        response = self.bot_client.get(view)
        self.assertEqual(len(response.context.get('page_obj')), 0)


class PostsPaginatorViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='elliot')
        cls.group = Group.objects.create(
            title='Мистер робот',
            slug='mr-robot',
            description='Сделать мир лучше',
        )
        cls.posts = []
        for num in range(20):
            cls.posts.append(
                Post(
                    author=cls.user,
                    text=f'Привет, {num}й друг',
                    group=cls.group,
                )
            )
        Post.objects.bulk_create(cls.posts)

        cls.PAGINATOR_GROUP_VIEW = reverse(
            'posts:group_list', kwargs={'slug': cls.group.slug}
        )
        cls.PAGINATOR_PROFILE_VIEW = reverse(
            'posts:profile', kwargs={'username': cls.user.username}
        )

    def setUp(self):
        self.guest_client = Client()

    def test_posts_views_paginator_10_posts_per_page(self):
        """Проверяем, что для всех релевантных views пагинатор слайсит
        по 10 постов на страницу."""
        paginator_views_config = (
            INDEX_VIEW,
            self.PAGINATOR_GROUP_VIEW,
            self.PAGINATOR_PROFILE_VIEW,
        )
        for view in paginator_views_config:
            with self.subTest(view=view):
                response = self.guest_client.get(view)
                self.assertEqual(
                    len(response.context.get('page_obj')), OBJECTS_PER_PAGE
                )
                response = self.guest_client.get(view + '?page=2')
                self.assertEqual(
                    len(response.context.get('page_obj')), OBJECTS_PER_PAGE
                )
