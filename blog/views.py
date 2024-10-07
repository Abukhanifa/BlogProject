from datetime import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Post
from .forms import PostForm, CommentForm

def posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'post_list.html', {"posts": posts})
    else:
        messages.success(request, "Error!")
        return render(request, 'home.html')
        

def post_new(request, pk=None):
    if request.user.is_authenticated:
        if pk:
            post = get_object_or_404(Post, pk=pk)
            form = PostForm(instance=post) 
        else:
            post = None
            form = PostForm()  

        if request.method == "POST":
            form = PostForm(request.POST, instance=post) 
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user  
                post.save()
                messages.success(request, "Post saved successfully!")
                return redirect('post_detail', post_id=post.pk)  

        return render(request, 'post_form.html', {"form": form, "post": post})  

    messages.error(request, "You must be logged in to create or edit posts.")
    return redirect('home')  


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.posts.all()  

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if request.user.is_authenticated:
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user  
                comment.save()
                return redirect('post_detail', post_id=post.id)  
    else:
        comment_form = CommentForm()  

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })
    
    
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)  
    if request.user != post.author:  
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('post_detail', post_id=post.id)  

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  
        if form.is_valid():
            form.save()  
            messages.success(request, "Post updated successfully!")
            return redirect('post_detail', post_id=post.id) 
    else:
        form = PostForm(instance=post)  

    return render(request, 'post_edit.html', {"form": form, "post": post})  


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)  
    if request.user != post.author:  
        messages.error(request, "You are not allowed to delete this post.")
        return redirect('post_detail', post_id=post.id) 

    if request.method == "POST":
        post.delete()  
        messages.success(request, "Post deleted successfully!")
        return redirect('home')  

    return render(request, 'post_delete.html', {"post": post})  

    
    



