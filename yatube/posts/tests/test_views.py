from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from ..models import Group, Post

User = get_user_model()


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
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': self.user.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id': self.post.pk}
            ): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': self.post.pk}
            ): 'posts/create_post.html',
        }
        for name, template in namespace_names.items():
            with self.subTest(name=name):
                response = self.authorized_client.get(name)
                self.assertTemplateUsed(response, template)

    def test_posts_index_page_valid_context(self):
        """Проверяем, что во view элемента главной страницы отрисован
        правильный context."""
        response = self.guest_client.get(reverse('posts:index'))
        self.context_validation_config(response.context['page_obj'][0])

    def test_posts_group_page_valid_context(self):
        """Проверяем, что во view элемента страницы группы отрисован
        правильный context."""
        response = self.guest_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(response.context['group'], self.group)
        self.context_validation_config(response.context['page_obj'][0])

    def test_posts_profile_page_valid_context(self):
        """Проверяем, что во view элемента страницы профиля отрисован
        правильный context."""
        response = self.guest_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.context['author'], self.user)
        self.context_validation_config(response.context['page_obj'][0])

    def test_posts_post_page_valid_context(self):
        """Проверяем, что во view страницы просмотра сообщения отрисован
        правильный context."""
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        self.context_validation_config(response.context['post'])

    def test_posts_create_edit_page_valid_context(self):
        """Проверяем, что во view страницы создания/редактирования сообщения
        отрисована форма с правильным context."""
        context_config = (
            reverse('posts:post_create'),
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
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

    def test_posts_new_post_renders_at_relevant_page(self):
        """Проверяем, что во views главной страницы, страницы группы
        и профиле автора отрисовано новое сообщение автора
        с правильным context."""
        views_config = (
            reverse('posts:index'),
            reverse(
                'posts:group_list', kwargs={'slug': self.author_group.slug}
            ),
            reverse(
                'posts:profile', kwargs={'username': self.author.username}
            ),
        )
        for view in views_config:
            with self.subTest(view=view):
                response = self.author_client.get(view)
                self.assertEqual(response.context['page_obj'][0], self.post)

    def test_posts_new_post_no_render_at_irrelevant_page(self):
        """Проверяем, что во view страницы нецелевой группы новое целевое
        сообщение автора не отрисовано."""
        view = reverse(
            'posts:group_list', kwargs={'slug': self.bot_group.slug}
        )
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

    def setUp(self):
        self.guest_client = Client()

    def test_posts_views_paginator_10_posts_per_page(self):
        """Проверяем, что для всех релевантных views пагинатор слайсит
        по 10 постов на страницу."""
        paginator_views_config = (
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user.username}),
        )
        for view in paginator_views_config:
            with self.subTest(view=view):
                response = self.guest_client.get(view)
                self.assertEqual(len(response.context.get('page_obj')), 10)
                response = self.guest_client.get(view + '?page=2')
                self.assertEqual(len(response.context.get('page_obj')), 10)
