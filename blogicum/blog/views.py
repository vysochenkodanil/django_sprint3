from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404
from .models import Post, Category


def index(request):
    current_time = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': posts})


def category_posts(request, category_slug):
    current_time = timezone.now()
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("Категория не опубликована")
    posts = Post.objects.filter(
        category=category,
        pub_date__lte=current_time,
        is_published=True
    ).order_by('-pub_date')
    return render(
        request, 'blog/category.html',
        {'category': category, 'post_list': posts}
    )


def post_detail(request, pk):
    current_time = timezone.now()
    post = get_object_or_404(Post, pk=pk)
    if (
        post.pub_date > current_time
        or not post.is_published
        or not post.category.is_published
    ):
        raise Http404("Публикация не найдена или недоступна")
    return render(request, 'blog/detail.html', {'post': post})
