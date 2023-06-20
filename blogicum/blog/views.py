from django.http import HttpResponseNotFound
from django.shortcuts import get_list_or_404, get_object_or_404, render
from blog.models import Post
import datetime


def index(request):
    template = 'blog/index.html'
    posts_list = Post.objects.values(
        'id', 'category__title', 'category__slug',
        'text', 'author__username', 'location',
        'location__name', 'location__is_published',
        'title', 'pub_date'
    ).filter(
        is_published=True, category__is_published=True,
        pub_date__date__lte=datetime.datetime.now()
    )
    context = {
        'posts_list': posts_list
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.objects.values(
        'title', 'location', 'location__is_published',
        'location__name', 'author__username',
        'category__title', 'category__slug', 'text'
    ).filter(
        pub_date__date__lte=datetime.datetime.now(),
        is_published=True, category__is_published=True
    ), pk=id)
    context = {
        'post': post
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    posts_list = get_list_or_404(Post.objects.values(
        'category__title', 'category__slug', 'category__description',
        'title', 'pub_date', 'location', 'location__is_published',
        'location__name', 'author__username', 'text', 'id'
    ).filter(
        is_published=True, category__slug=category_slug,
        category__is_published=True,
        pub_date__date__lte=datetime.datetime.now()
    ))
    context = {
        'category': category_slug,
        'posts_list': posts_list
    }
    return render(request, template, context)