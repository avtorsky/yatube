from re import T
import shutil
import tempfile
from http import HTTPStatus

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Group, Post, User

POST_CREATE_VIEW = reverse('posts:post_create')
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
PIXEL = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
NOT_A_PIXEL = b''


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
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
        cls.pixel_uploaded = SimpleUploadedFile(
            name='test_pixel.gif', content=PIXEL, content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Привет, друг',
            group=cls.group,
            image=cls.pixel_uploaded,
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
        cls.POST_COMMENT_VIEW = reverse(
            'posts:add_comment', kwargs={'post_id': cls.post.pk}
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_posts_form_is_vaild(self):
        """Проверяем, что форма использует валидный context."""
        response = self.authorized_client.get(POST_CREATE_VIEW)
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
            'image': self.post.image,
        }
        response = self.authorized_client.post(
            POST_CREATE_VIEW,
            data=form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Post.objects.count(), posts_db_count + 1)
        self.assertTrue(
            Post.objects.filter(
                author=self.post.author,
                text=self.post.text,
                group=self.post.group.pk,
                image='posts/test_pixel.gif',
            ).exists(),
            Post.objects.latest('pub_date'),
        )
        self.assertRedirects(
            response,
            self.PROFILE_VIEW,
        )

    def test_posts_broken_image_form_dont_creates_new_post_entry_in_db(self):
        """Проверяем, что при отправке невалидной формы со страницы создания поста
        новая запись в базе данных не создаётся."""
        broken_pixel_uploaded = SimpleUploadedFile(
            name='test_broken_pixel.txt',
            content=NOT_A_PIXEL,
            content_type='text/plain',
        )
        form_data = {
            'text': 'Привет, битый друг',
            'image': broken_pixel_uploaded,
        }
        self.authorized_client.post(
            POST_CREATE_VIEW,
            data=form_data,
            follow=True,
        )
        post = Post.objects.filter(
            author=self.user, image=form_data['image']
        ).first()
        self.assertIsNone(post)

    def test_posts_valid_form_edit_post_entry_in_db(self):
        """Проверяем, что при отправке валидной формы со страницы
        редактирования поста происходит изменение поста в базе данных."""
        form_data = {
            'text': 'Привет, отредактированный друг.',
        }
        response = self.authorized_client.post(
            self.POST_EDIT_VIEW,
            data=form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, form_data['text'])
        self.assertRedirects(
            response,
            self.POST_DETAIL_VIEW,
        )

    def test_posts_comment_view_in_valid_context(self):
        """Проверяем, что комментарий после отправки формы отрисован
        во view страницы просмотра соответствующего сообщения."""
        form_data = {
            'text': 'Контроль — это иллюзия',
        }
        response = self.authorized_client.post(
            self.POST_COMMENT_VIEW, data=form_data, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Comment.objects.filter(
                post=self.post.pk,
                text=form_data['text'],
            ).exists(),
            Comment.objects.latest('created'),
        )
