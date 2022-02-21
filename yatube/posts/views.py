from django.shortcuts import get_object_or_404, render

from .models import Group, Post


def index(request):
    template = 'posts/index.html'
    text = 'Новостная лента проекта Yatube'
    posts = Post.objects.filter()[:10]
    context = {
        'text': text,
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    text = f'Новости группы {slug} на Yatube'
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_post.all()[:10]
    context = {
        'text': text,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
