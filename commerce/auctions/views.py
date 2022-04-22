from decimal import Decimal
from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import AuctionListing
from .models import Bids
import logging

def index(request):
    listings= AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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

def new_listing(request):
    if request.method == "POST":
        title = request.POST["listing_title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image"]        
        
        al = AuctionListing(
            name = title,
            description = description,
            starting_bid = starting_bid,
            image = image,
            caller = get_user(request).username
        )

        al.save()
        return render(request, "auctions/index.html")
        
    else:        
        return render(request, "auctions/newlisting.html")

def listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    highest_bid = Bids(price=0)
    message = ""

    if(Bids.objects.count() > 0):
        highest_bid = Bids.objects.all()[0]

    if request.method == "POST":
        bid = Decimal(request.POST["bid_amount"])
        auction = listing

        if Bids.objects.count() > 0:
            if highest_bid.price < bid:
                highest_bid.price = bid
                highest_bid.bidder = get_user(request).username  
                highest_bid.save()
                message = "Updated highest bid"
            else:
                message = "Bid should be higher than the current"
        else:
            if bid > listing.starting_bid: 
                newbid = Bids(
                    price = bid,
                    auction_listing = auction,
                    bidder = get_user(request).username
                )  
                newbid.save()
                message = "First bid!"
            else:
                message = "Bid should be higher than the starting bid"
    
    return render(request, "auctions/listing.html", {
        "highest_bid": highest_bid.price,
        "listing": listing,
        "message": message
    })