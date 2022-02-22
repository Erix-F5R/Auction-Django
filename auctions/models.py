from sre_parse import CATEGORIES
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Auction(models.Model):

    AUTO = 'aut'
    BOOK = 'boo'
    CLOTHES = "clo"
    ELEC = 'ele'
    HOME = 'hom'
    MUSIC = 'mus'
    SPORT = 'spo'
    TOYS = 'toy'

    CATEGORIES = [(AUTO, "Automotive"),
                (BOOK, "Books"),
                (CLOTHES, "Clothing"),
                (ELEC, "Electronic"),
                (HOME, "Home and Garden"),
                (MUSIC, "Music"),
                (SPORT, "Sports and Outdoors"),
                (TOYS, "Toys and Games")]

    title = models.CharField(max_length=100)
    text = models.TextField(default = "Write a description here.")
    category = models.CharField(max_length = 3, choices = CATEGORIES, default = AUTO)
    url = models.URLField(null=True, blank=True)
    min_bid = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField(default=datetime.now, blank=True, null= True)
    closed = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now, blank=True, null= True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, blank=True , null= True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True , null= True)

    def __str__(self):
        return f"{self.auction}: ${self.amount}"

class Comment(models.Model):

    text = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now, blank=True, null= True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

class Watchlist(models.Model):

    user = models.ForeignKey(User, on_delete= models.CASCADE , related_name="watchlist")
    auction = models.ForeignKey(Auction, on_delete= models.CASCADE)

    def __str__(self):
        return f"{self.user}: {self.auction}"