from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date') # lte = less than or equal to
    return render(request, 'blog/post_list.html', {'posts': posts}) # request = everything we receive from the user via the internet; url is the template file; {} = things for the template to use

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # not ready to commit yet
            post.author = request.user # add the author here since there was no field in the form
            post.published_date = timezone.now() # default publish date is when it's submitted
            post.save() # this commits the save
            return redirect('post_detail', pk=post.pk) # this is the name of the view we want to go to
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

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
    return render(request, 'blog/post_edit.html', {'form': form})
