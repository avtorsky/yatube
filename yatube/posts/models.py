from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('Человекопонятный URL', unique=True)
    description = models.TextField('Описание группы')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Напечатайте сообщение',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор сообщения',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='group_post',
        help_text='Выберите группу для публикации сообщения',
        verbose_name='Группа сообщения',
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = tuple(['-pub_date'])
        verbose_name_plural = 'Посты'
