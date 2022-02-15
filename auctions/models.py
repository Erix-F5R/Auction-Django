from sre_parse import CATEGORIES
from django.contrib.auth.models import AbstractUser
from django.db import models


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
    url = models.URLField(blank=True)
    min_bid = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Bid(models.Model):
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

class Comment(models.Model):

    text = models.CharField(max_length=100)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)