from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Group, Post, User
from .forms import PostForm

OBJECTS_PER_PAGE = settings.PAGINATOR_SLICING_CONFIG


def index(request):
    template = 'posts/index.html'
    text = 'Новостная лента проекта Yatube'
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'text': text,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    text = f'Новости группы {slug} на Yatube'
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.group_post.all()
    paginator = Paginator(posts_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'text': text,
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    text = 'Профайл пользователя'
    profile = get_object_or_404(User, username=username)
    posts_list = profile.posts.all()
    paginator = Paginator(posts_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'text': text,
        'author': profile,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    context = {
        'form': form,
    }
    if not form.is_valid():
        return render(request, template, context)

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', username=request.user.username)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, instance=post)
    context = {'form': form, 'post_id': post_id, 'is_edit': True}
    if not form.is_valid():
        return render(request, template, context)
    form.save()
    return redirect('posts:post_detail', post_id=post_id)
