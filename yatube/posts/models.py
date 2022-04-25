from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('Человекопонятный URL', unique=True)
    description = models.TextField('Описание группы')

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст сообщения',
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
    image = models.ImageField(
        'Иллюстрация сообщения', upload_to='posts/', blank=True, null=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Прокомментированное сообщение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Напечатайте комментарий',
    )
    created = models.DateTimeField(
        'Дата и время комментария', auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор в подписке',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name='profile_follow_rule'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_follow_rule',
            ),
        ]
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return self.user.username
