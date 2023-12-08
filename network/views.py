from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User, Post, Fallow, Like


def index(request):
    user=request.user
    allPosts = Post.objects.all().order_by("date").reverse()
    likeList=[]
    
    #Get the users all liked posts
    if user.is_authenticated:
        userLikes= Like.objects.filter(user=user)
        for likedPost in userLikes:
            likeList.append(likedPost.post.id)

    
    #Pagination
    paginator = Paginator(allPosts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
            "page_obj": page_obj,
            "user":user,
            "likeList":likeList
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def makePost(request):
    #Creating a new post
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(pk= request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))
    
    
def userProfile(request, username):
    user= request.user
    
    #Get the profile of a user and all posts
    profile = User.objects.get(username=username)
    fallowers = Fallow.objects.filter(fallowed=profile)
    fallows = Fallow.objects.filter(fallowing=profile)
    userPosts = Post.objects.filter(user=profile.id).order_by("date").reverse()
    myList=[]
    likeList=[]
    buttonValue="Fallow"

    paginator = Paginator(userPosts, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #check if current user is fallowing this profile 
    if user.is_authenticated:
        fallowedUsers = Fallow.objects.filter(fallowing=user)
        for fallowedUser in fallowedUsers:
            myList.append(fallowedUser.fallowed)
            
        for i in myList:
            if str(username) == str(i):
                buttonValue="Unfallow"
                break
        
        #get likes
        userLikes= Like.objects.filter(user=user)
        for likedPost in userLikes:
            likeList.append(likedPost.post.id) 
    
    return render(request, "network/userProfile.html", {
        "profile":username,
        "fallowers":len(fallowers),
        "fallows":len(fallows),
        "page_obj":page_obj,
        "user": user,
        "buttonValue" :buttonValue,
        "likeList": likeList,
    })

@login_required(login_url='login')
def fallowing(request):
    user = request.user
    fallowedUsers = Fallow.objects.filter(fallowing=user)
    myList=[]
    sets =[]
    allPosts=[]
    likeList=[]

    #get all the fallowed users then get all of those users posts
    for fallowedUser in fallowedUsers:
        myList.append(fallowedUser.fallowed)
           
    for i in myList: 
        sets.append(Post.objects.filter(user=i))
    
    for queryset in sets:
        for post in queryset:
            allPosts.append(post)
    #sort the posts by using the date
    allPosts = sorted(allPosts, key=lambda x: x.date, reverse=True)

    #get likes
    userLikes= Like.objects.filter(user=user)
    for likedPost in userLikes:
        likeList.append(likedPost.post.id)

    print(likeList)
    

    paginator = Paginator(allPosts, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/fallowing.html", {
        "page_obj":page_obj,
        "likeList": likeList       
    })

@login_required(login_url='login')
def fallowUser(request):
    if request.method == "POST":
        user = User.objects.get(pk= request.user.id)
        profile = request.POST["profile"]
        userToFallow= User.objects.get(username = profile)
        if request.POST["action"] == "Fallow":
            fallow = Fallow(fallowing=user, fallowed=userToFallow)
            fallow.save()
        else:
            unfallow = Fallow.objects.filter(fallowing=user, fallowed=userToFallow)
            unfallow.delete()

        return HttpResponseRedirect(reverse(index))

@login_required(login_url='login')   
def editPost(request, post_id):
    
    data = json.loads(request.body)
    post = Post.objects.get(id=post_id)
    post.content=data["content"]
    post.save()
    
    return HttpResponse(status=200)

@login_required(login_url='login')
def likePost(request, post_id, action):    
    user = User.objects.get(pk= request.user.id)
    post= Post.objects.get(id = post_id)
    if action == "Like":
        #check if user already liked that post
        if Like.objects.filter(user=user, post=post).exists():
            return HttpResponse(status=400)
        else:
            like = Like(user=user, post=post)
            like.save()
    else:  
        #check if user already un-liked that post
        if Like.objects.filter(user=user, post=post).exists():
            unlike = Like.objects.filter(user=user, post=post)
            unlike.delete()
        else:
            return HttpResponse(status=400)
    return HttpResponse(status=200)