from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, categories, listings, bids, comments


def index(request):
    
    return render(request, "auctions/index.html", {
        "listings" : listings.objects.all(),

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        lister = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        min_bid = request.POST["min_bid"]
        image = request.POST.get("image", "")
        category = request.POST.get("category", "")
        if category != "":
            catdata = categories.objects.get(categories=category)
        else:
            catdata =  None



        newlisting = listings( 
            lister=lister,
            title=title,
            description=description,
            min_bid=int(min_bid),
            image=image,
            category=catdata
        )
        newlisting.save()
        return HttpResponseRedirect(reverse(index))




    category_name= categories.objects.all()
    return render(request, "auctions/create_listing.html",{
        "categories": category_name
    })

def view_listing(request, listing_id):
    user = request.user
    listing = listings.objects.get(id = listing_id)

    if user == listing.lister:
        if listing.active == True:
            owner = True
        else: 
            owner= False
    else:
        owner= False

    no_bids = True
    if listing.get_bid.all().exists():
        no_bids = False
        bidall= listing.get_bid.all()
        bid= bidall[len(bidall)-1]
    else:  
        bid = "No bids made yet."

    won = False
    closed_before_bid = False
    if listing.active == False:
        if no_bids:
            closed_before_bid = True
        try:
            if user == bid.bidder:
                won = True
        except:
            pass       


    comments= listing.get_comment.all()
    
    inwatchlist = False
    loggedin = False
    if request.user.is_authenticated:
        loggedin = True
        
    if user in listing.watchlist.all():
        inwatchlist = True
        
    return render(request, "auctions/listing.html",{
        "loggedin": loggedin,
        "listing" : listing,
        "inwatchlist": inwatchlist,
        "top_bid": bid,
        "comments": comments,
        "owner": owner,
        "won": won,
        "list_status": listing.active,
        "closed_before_bid": closed_before_bid
    })

@login_required(login_url='login')
def edit_watchlist(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = listings.objects.get(id = listing_id)
        if user in listing.watchlist.all():
            listing.watchlist.remove(user)
            listing.save()
        
        else:
            listing.watchlist.add(user)
            listing.save()
        return HttpResponseRedirect(reverse("view_listing",args=(listing.id, )))

@login_required(login_url='login')    
def bid(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = listings.objects.get(pk = listing_id)
        new_bid= int(request.POST["bid"])
        
        if listing.get_bid.all().exists():
            bidall= listing.get_bid.all()
            amount= bidall[len(bidall)-1]
            min_bid=int(str(amount))
        else:
            min_bid= int(listing.min_bid)

        if new_bid > min_bid:
            
            b = bids(
                bidder = user,
                amount = new_bid,
                product = listing
            )
            b.save()
            return HttpResponseRedirect(reverse("view_listing",args=(listing.id, )))
        else:
            return render(request, "auctions/error_bid.html",{
        "list_id": listing.id
    })
            
        
            
 
    
@login_required(login_url='login')
def comment(request,listing_id):
    if request.method == "POST":
        user = request.user
        listing = listings.objects.get(pk = listing_id)
        comment_text = request.POST["comment"]
        c = comments(
            commentor= user,
            comment_text= comment_text,
            listing= listing
        )
        c.save()


    return HttpResponseRedirect(reverse("view_listing",args=(listing.id, )))

@login_required(login_url='login')
def close_listing(request, listing_id):
    if request.method == "POST":
        listing = listings.objects.get(pk = listing_id)
        listing.active = False
        listing.save()

    return HttpResponseRedirect(reverse("view_listing",args=(listing.id, )))


@login_required(login_url='login')
def list_watchlist(request):
    user = request.user
    watchlist= user.watchlisting.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist" : watchlist,
        })

def all_categories(request):
    return render(request, "auctions/categories.html", {
        "categories": categories.objects.all()
        })

def view_category(request, category_id ):

    category= categories.objects.get(pk = category_id)
    rel_listings= category.get_category.all()

    return render(request, "auctions/related_listings.html", {
        "rel_listings": rel_listings
        })
