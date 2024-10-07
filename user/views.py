from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Follow
from .forms import ProfileForm, SignUpForm
from blog.forms import PostForm
from blog.models import Post
from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    posts = Post.objects.all() 
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user  
                post.save()
                messages.success(request, "Posted Successfully!")
                return redirect('home')  
        else:
            form = PostForm()  

        return render(request, 'home.html', {"posts": posts, "form": form}) 

    return render(request, 'home.html', {"posts": posts}) 

        
def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In!"))
            return redirect("home")
        else:
            messages.success(request, ("Error! Please Try Again!"))
            return redirect("login")
        
    else:
        return render(request, 'login.html', {})
    
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You Successfully Logged Out!"))
    return redirect('home')


def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            Profile.objects.create(user=user)
            messages.success(request, ("You Successfully Registered"))
            return redirect('home')
    return render(request, 'registration.html', {'form': form})


def profile_view(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        followers = Follow.objects.filter(following=profile.user)
        followings = Follow.objects.filter(follower=profile.user)
        posts = Post.objects.filter(author=profile.user)
        is_following = Follow.objects.filter(follower=request.user, following=profile.user).exists()
        if profile.user == request.user:
            is_self = True
        else:
            is_self = False
        if request.method == "POST":
            action = request.POST.get('follow')
            if not is_self: 
                if action == "unfollow":
                    Follow.objects.filter(follower=request.user, following=profile.user).delete()
                    messages.success(request, f"You have unfollowed {profile.user.username}.")
                else:
                    Follow.objects.get_or_create(follower=request.user, following=profile.user)
                    messages.success(request, f"You are now following {profile.user.username}.")
            else:
                messages.error(request, "You cannot follow or unfollow yourself.")          
            return redirect('profile_view', pk=profile.user.pk)  
        return render(request, 'profile.html', {
            'profile': profile,
            'followers': followers,
            'followings': followings,
            'is_following': is_following,  
            'is_self': is_self,  
            'posts': posts,  
        })
    else:
        messages.error(request, "You must be logged in!")
        return redirect("home")
    
    
def people(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'people.html', {"profiles": profiles})
    else:
        messages.success(request, ("You Must Be Logged In"))
        return redirect('home')       
    
    
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)  
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=profile)  
            if form.is_valid():
                form.save()  
                messages.success(request, "Profile updated successfully!")  
                return redirect('profile_view', pk=request.user.pk)  
        else:
            form = ProfileForm(instance=profile)  

    return render(request, 'edit_profile.html', {'form': form})  
    
    
    