from tkinter import CASCADE
from tokenize import String
from unicodedata import decimal
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):    
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.CharField(max_length=255)
    caller = models.CharField(max_length=50)

class Bids(models.Model):
    bidder = models.CharField(max_length=50)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)

class Comment(models.Model):
    commenter = models.CharField(max_length=50)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
