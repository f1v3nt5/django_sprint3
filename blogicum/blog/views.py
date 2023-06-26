from datetime import datetime

from django.shortcuts import get_list_or_404, get_object_or_404, render

from blog.models import Post, Category


POSTS_COUNT = 5


def post_pub_filter():
    return Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    ).select_related(
        'location', 'category', 'author'
    )


def index(request):
    post_list = post_pub_filter().order_by('-pub_date')[:POSTS_COUNT]
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(post_pub_filter(), pk=id)
    context = {
        'post': post
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, is_published=True,
        slug=category_slug)
    post_list = category.categories.filter(
        is_published=True,
        pub_date__lte=datetime.now()
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
