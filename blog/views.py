from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from functools import reduce
from operator import and_

counter = 0

# Create your views here.

def post_list(request, query = ''):
    global counter
    counter += 1
    print(counter)
    if request.method == "POST":
        query = request.POST['q']
        print(query)

    words = parse_search_params(query)
    if query != '':
        or_lookup = reduce(and_,[(Q(text__icontains = p)|Q(words__icontains = p)|Q(title__icontains = p))&Q(published_date__lte = timezone.now()) for p in words])

        posts = Post.objects.filter(or_lookup)
    else:
        posts = Post.objects.filter(published_date__lte = timezone.now())
    # posts = Post.objects.filter(
    #     Q(text__icontains = query)&Q(published_date__lte = timezone.now())
    # )
    posts = posts.order_by('published_date')
    print('call post_list')
    return render(request, 'blog/post_list.html', {'posts' : posts})

def parse_search_params(words: str):
        search_words = words.replace('　', ' ').split()
        return search_words



def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    print('call post_new')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            # if(len(post.text) > 50):
            #     post.shortText = post.text[0:50]
            # else:
            #     post.shortText = post.text

            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    print('call post_edit')
    post = get_object_or_404(Post, pk = pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance = post)
        if form.is_valid():
            post = form.save(commit = False)
            print(len(post.text))
            # if(len(post.text) > 50):
            #     post.shortText = post.text[0:50]
            # else:
            #     post.shortText = post.text

            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)

    else:
        form = PostForm(instance = post)

    return render(request, 'blog/post_edit.html',{'form': form})
