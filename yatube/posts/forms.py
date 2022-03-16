from django import forms
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea,
        label='Текст сообщения',
        required=True,
        help_text='Напечатайте или отредактируйте сообщение',
    )

    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {'group': 'Группа сообщения'}
        help_texts = {'group': 'Выберите группу для публикации сообщения'}
