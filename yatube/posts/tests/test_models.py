from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostsModelsTest(TestCase):
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

    def test_posts_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает метод __str__."""
        post = PostsModelsTest.post
        expected_post_object_name = post.text[:15]
        self.assertEqual(expected_post_object_name, str(post))

        group = PostsModelsTest.group
        expected_group_object_name = group.title
        self.assertEqual(expected_group_object_name, str(group))

    def test_posts_post_model_has_text_annotation(self):
        """Проверяем, что help_text поля text совпадает с ожидаемым."""
        post = PostsModelsTest.post
        expected_help_text = post._meta.get_field('text').help_text
        self.assertEqual(expected_help_text, 'Напечатайте сообщение')

    def test_posts_post_model_has_author_label(self):
        """Проверяем, что verbose_name поля author совпадает с ожидаемым."""
        post = PostsModelsTest.post
        expected_verbose_name = post._meta.get_field('author').verbose_name
        self.assertEqual(expected_verbose_name, 'Автор сообщения')

    def test_posts_post_model_has_group_annotation(self):
        """Проверяем, что help_text поля group совпадает с ожидаемым."""
        post = PostsModelsTest.post
        expected_help_text = post._meta.get_field('group').help_text
        self.assertEqual(
            expected_help_text, 'Выберите группу для публикации сообщения'
        )

    def test_posts_post_model_has_group_label(self):
        """Проверяем, что verbose_name поля group совпадает с ожидаемым."""
        post = PostsModelsTest.post
        expected_verbose_name = post._meta.get_field('group').verbose_name
        self.assertEqual(expected_verbose_name, 'Группа сообщения')
