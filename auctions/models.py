from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
    title = models.CharField(max_length=100)
    min_bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Bid(models.Model):
    
    amount = models.FloatField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

class Comment(models.Model):

    text = models.CharField(max_length=100)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)