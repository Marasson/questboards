import django.contrib.auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm, CommentForm
from .models import Post, Comment


def post_list(request):
    object_list = Post.objects.filter(
        published_date__lte=timezone.now())  # Posts.object.all() - wyswietla wszystkie obiekty post - created i publish
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    query = request.GET.get("q")
    if query:
        object_list = object_list.filter(
            Q(title__icontains=query)
        )

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:

        # If page is not an integer deliver the first page

        posts = paginator.page(1)
    except EmptyPage:

        # If page is out of range deliver last page of results

        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'my_project/post_list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'my_project/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'my_project/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'my_project/post_edit.html', {'form': form})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'my_project/post_draft_list.html', {'posts': posts})


def logout_page(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect("/")


def about(request):
    return render(request, 'my_project/about.html', {'about': about})


def register_f(request):
    return render(request, 'my_project/register_f.html', {'register_f': register_f})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('base')
    else:
        form = UserCreationForm()
    return render(request, 'my_project/register_f.html', {'form': form})


def search(request):
    return render(request, 'my_project/search.html', {'search': search})


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'my_project/add_comment_to_post.html', {'form': form})


def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)



