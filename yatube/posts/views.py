from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User

OBJECTS_PER_PAGE = settings.PAGINATOR_SLICING_CONFIG
CACHE_KEY = settings.POSTS_INDEX_CACHE_KEY


def index(request):
    template = 'posts/index.html'
    text = 'Новостная лента проекта Yatube'
    posts_list = cache.get(CACHE_KEY)
    if posts_list is None:
        posts_list = Post.objects.all()
        cache.set(CACHE_KEY, posts_list, timeout=20)
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
    following = request.user.is_authenticated and Follow.objects.filter(
        author=profile,
        user=request.user,
    )
    followers_count = Follow.objects.filter(author=profile).count()
    context = {
        'text': text,
        'author': profile,
        'page_obj': page_obj,
        'paginator': paginator,
        'following': following,
        'followers_count': followers_count,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('post')
    form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
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

    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    context = {'form': form, 'post_id': post_id, 'is_edit': True}
    if not form.is_valid():
        return render(request, template, context)
    form.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, id=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    text = f'Избранные авторы пользователя {request.user.username}'
    posts_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'text': text,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(
            author=author,
            user=request.user,
        )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(author=author, user=request.user).delete()
    return redirect('posts:profile', username=username)
