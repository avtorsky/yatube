from django import forms
from django.forms import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea,
        label='Текст сообщения',
        required=True,
        help_text='Напечатайте или отредактируйте сообщение',
    )

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea,
        label='Текст комментария',
        required=True,
        help_text='Напечатайте или отредактируйте комментарий',
    )

    class Meta:
        model = Comment
        fields = ('text',)
