from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, Auction, Bid, Watchlist
from .forms import NewBidForm, NewListingForm


def index(request):
    return render(request, "auctions/index.html", {"activeListings": Auction.objects.all()})


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

@login_required(login_url='/login')
def create_listing(request):

    if request.method == 'POST':

        form = NewListingForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            category = form.cleaned_data["category"]
            url = form.cleaned_data["url"]
            min_bid = form.cleaned_data["min_bid"]

            auction = Auction(title=title,
                              user=User.objects.get(pk=request.user.id),
                              text=text,
                              category=category,
                              min_bid=min_bid,
                              url=url)

            auction.save()
    # If method == GET return default form
    else:
        return render(request, "auctions/create-listing.html", {
            "form": NewListingForm()})

    # Where to redirect after?
    return render(request, "auctions/create-listing.html", {"form": NewListingForm()})

@login_required(login_url='/login')
def auction(request, auction_id):

    auction = Auction.objects.get(id=auction_id)
    highest_bidder = Bid.objects.filter(auction = auction).last()
    
    try:
        highest_bid = Bid.objects.filter(auction = auction).last()
    except:
        highest_bid = auction.min_bid

    ## if no bids
    ##try:
    ##    max_bid = float( Bid.objects.filter(auction = auction).aggregate(Max('amount'))['amount__max'])
    ##except:
    ##    max_bid = auction.min_bid

    if request.method == "POST":

        if request.POST.get("submit") == "Bid":

            form = NewBidForm(request.POST)

            if form.is_valid():
                amount = form.cleaned_data['amount']

                if amount <= max_bid or amount <= auction.min_bid :
                    return render(request, "auctions/auction.html", {"auction": auction, "form": NewBidForm(), "error":'Error, invaild bid', "highest_bid": highest_bid})

                bid = Bid(amount=amount,
                          user=User.objects.get(id=request.user.id),
                          auction=Auction.objects.get(pk=auction_id))
                bid.save()
            return render(request, "auctions/auction.html", {"auction": auction, "form": NewBidForm(), "error": '', "highest_bid": highest_bid})

        elif request.POST.get("submit") == "Watchlist":
            user = User.objects.get(id=request.user.id)

            if not user.watchlist.filter(auction=auction):
                watchlist = Watchlist(user=User.objects.get(id=request.user.id),
                                      auction=Auction.objects.get(pk=auction_id))
                watchlist.save()

            else:
                user.watchlist.filter(auction=auction).delete()

            return render(request, "auctions/auction.html", {"auction": auction, "form": NewBidForm(), "error": '' , "highest_bid": highest_bid})

        elif request.POST.get("submit") == "Close Auction":

            auction.closed = True
            auction.save()

            return render(request, "auctions/auction.html", {"auction": auction, "form": NewBidForm(), "error": '' , "highest_bid": highest_bid})

    else:
        return render(request, "auctions/auction.html", {"auction": auction, "form": NewBidForm(), "error": '', "highest_bid": highest_bid})


@login_required(login_url='/login')
def watchlist(request):

    user = User.objects.get(id=request.user.id)

    watchlist = Watchlist.objects.filter(user=user)

    return render(request, "auctions/watchlist.html", {"watchlist": watchlist})


def categories(request):

    categories = Auction.CATEGORIES

    return render(request, "auctions/categories.html", {"categories": categories})


def category(request, category):

    items = Auction.objects.filter(category=category)

    return render(request, "auctions/category.html", {"category": category, "items": items})
