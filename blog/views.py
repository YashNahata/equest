from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post, BlogComment, PostImage

# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None, approved=True)
    replies = BlogComment.objects.filter(post=post, approved=True).exclude(parent=None)
    photos = PostImage.objects.filter(post=post)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    return render(request, 'blogPost.html', {"post": post, "comments": comments, "photos": photos, 'replyDict': replyDict})

def search(request):
    query = request.GET['q']
    if len(query) > 64:
        posts = Post.objects.none()
    else:
        postsTitle = Post.objects.filter(title__icontains=query)
        postsContent = Post.objects.filter(content__icontains=query)
        posts = postsTitle.union(postsContent)
    if posts.count() == 0:
        messages.warning(request, "No search results found")
    return render(request, 'search.html', {'posts': posts})

def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        firstName = request.POST['fname']
        lastName = request.POST['lname']     
        email = request.POST['signUpEmail']
        password1 = request.POST['signUpPassword1']
        password2 = request.POST['signUpPassword2']
        if len(username) > 16:
            messages.error(request, "Username must be under 16 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers")
            return redirect('home')
        if password1 != password2:
             messages.error(request, "Passwords do not match")
             return redirect('home')
        user = User.objects.create_user(username, email, password1)
        user.first_name = firstName
        user.last_name = lastName
        user.save()
        messages.success(request, "Your account has been successfully created. Please Login to continue.")
        return redirect('home')
    else:
        return HttpResponse("404 - Page not found")

def handleLogin(request):
    if request.method == "POST":
        username = request.POST['loginUsername']
        password = request.POST['loginPassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("home")
    else:
        return HttpResponse("404 - Page not found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        approved = request.POST.get('approved')
        if len(comment) < 1:
            messages.error(request, "Comment cannot be empty")
            return redirect(f"/{post.slug}")
        if len(comment) > 300:
            messages.error(request, "Comment must be less than 300 characters")
            return redirect(f"/{post.slug}")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post, approved=approved)
            comment.save()
            messages.success(request, "Your comment has been submitted successfully. Will be published after approval.")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post , parent=parent, approved=approved)
            comment.save()
            messages.success(request, "Your reply has been submitted successfully. Will be published after approval.")
        return redirect(f"/{post.slug}")