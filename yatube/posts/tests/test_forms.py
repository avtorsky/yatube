from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from http import HTTPStatus

from ..models import Group, Post

User = get_user_model()


class PostsFormTests(TestCase):
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

    def test_posts_form_is_vaild(self):
        """Проверяем, что форма использует валидный context."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertIsInstance(
            response.context['form'].fields['text'],
            forms.fields.CharField,
        )
        self.assertIsInstance(
            response.context['form'].fields['group'],
            forms.fields.ChoiceField,
        )

    def test_posts_valid_form_creates_new_post_entry_in_db(self):
        """Проверяем, что при отправке валидной формы со страницы создания поста
        создаётся новая запись в базе данных."""
        posts_db_count = Post.objects.count()
        form_data = {
            'author': self.post.author,
            'text': self.post.text,
            'group': self.post.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Post.objects.count(), posts_db_count + 1)
        self.assertTrue(
            Post.objects.filter(
                author=self.post.author,
                text=self.post.text,
                group=self.post.group.pk,
            ).exists()
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username}),
        )

    def test_posts_valid_form_edit_post_entry_in_db(self):
        """Проверяем, что при отправке валидной формы со страницы
        редактирования поста происходит изменение поста в базе данных."""
        form_data = {
            'text': 'Привет, отредактированный друг.',
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk},
            ),
            data=form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, form_data['text'])
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}),
        )
