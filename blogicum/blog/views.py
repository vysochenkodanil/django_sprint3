from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def index(request):
    current_time = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:settings.POSTS_PER_PAGE]
    return render(request, 'blog/index.html', {'post_list': posts})


def category_posts(request, category_slug):
    current_time = timezone.now()
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.filter(
        category=category,
        pub_date__lte=current_time,
        is_published=True
    ).order_by('-pub_date')
    return render(
        request, 'blog/category.html',
        {'category': category, 'post_list': posts}
    )


def post_detail(request, post_id):
    current_time = timezone.now()
    post = get_object_or_404(
        Post,
        pk=post_id,
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})
