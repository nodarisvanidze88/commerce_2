from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Catrgory, Listing

def listing(request, id):
    itemData = Listing.objects.get(pk=id)
    checkinWatchlist = request.user in itemData.watchList.all()
    return render(request, "auctions/listing.html",{
        "listingdata": itemData,
        "checkinwatchlist": checkinWatchlist,
    })
def removeFromWatchlist(request, id):
    listingItem = Listing.objects.get(pk=id)
    currentUser = request.user
    listingItem.watchList.remove(currentUser)
    return HttpResponseRedirect(reverse(listing,args=(id, )))

def addToWatchlist(request, id):
    listingItem = Listing.objects.get(pk=id)
    currentUser = request.user
    listingItem.watchList.add(currentUser)
    return HttpResponseRedirect(reverse(listing,args=(id, )))

def index(request):
    activeListing = Listing.objects.filter(isActive=True)
    allCategoris = Catrgory.objects.all()
    return render(request, "auctions/index.html",{
        "listings":activeListing,
        "allCategories":allCategoris
        })

def displayCategory(request):
    if request.method == "POST":
        selectedCategory = request.POST["category"]
        categoryInList = Catrgory.objects.get(categoryName=selectedCategory)
        activeListing = Listing.objects.filter(isActive=True, category=categoryInList)
        allCategoris = Catrgory.objects.all()
        return render(request, "auctions/index.html",{
            "listings":activeListing,
            "allCategories":allCategoris
            })

def createListing(request):
    if request.method == "GET":
        allCategoris = Catrgory.objects.all()
        return render(request, "auctions/create.html", {"allCategories":allCategoris})
    else:
        title = request.POST['title']
        description = request.POST['description']
        imageUrl = request.POST['imgurl']
        price = request.POST['price']
        category = request.POST['category']
        curentUser = request.user
        categoryData = Catrgory.objects.get(categoryName = category)

        newListing = Listing(
            title = title,
            description = description,
            imageUrl = imageUrl,
            price = float(price),
            category = categoryData,
            owner = curentUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
    
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
