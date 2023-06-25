from datetime import datetime

from django.shortcuts import get_list_or_404, get_object_or_404, render

from blog.models import Post, Category


POSTS_COUNT = 5


def post_pub_filter():
    return Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )


def index(request):
    post_list = post_pub_filter().select_related(
        'location', 'category', 'author'
    ).order_by('-pub_date')[:POSTS_COUNT]
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(post_pub_filter().select_related(
        'location', 'category', 'author'
    ), pk=id)
    context = {
        'post': post
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.values(
        'title', 'description', 'slug'
    ).filter(is_published=True,  slug=category_slug))
    post_list = Post.objects.filter(
        is_published=True,
        category__slug=category_slug,
        pub_date__lte=datetime.now()
    ).select_related('category').order_by(
        '-pub_date'
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
