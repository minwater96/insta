from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    posts = Post.objects.all()
    form = CommentForm()

    context = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()

    context = {
        'form': form,
    }

    return render(request, 'form.html', context)

@require_POST
@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()

        return redirect('posts:index')

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    # 이미 좋아요 버튼을 누른경우
    if user in post.like_users.all():
        post.like_users.remove(user)
    #아직 좋아요 버튼을 누르지 않은 경우
    else:
        post.like_users.add(user) #post.like_users.add(user) 같은효과

    return redirect('posts:index')

from django.http import JsonResponse

def like_async(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False
    else:
        post.like_users.add(user)
        status = True

    context = {
        'post_id': post_id,
        'status': status,
        'count': len(post.like_users.all())
    }

    return JsonResponse(context)
