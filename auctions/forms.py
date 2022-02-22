from django import forms
from .models import Auction, Bid, Comment, Watchlist



class NewListingForm(forms.ModelForm):
    
    class Meta:
        model = Auction
        fields = ['title', 'text', 'category', 'url', 'min_bid']

class NewBidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ['amount']

class NewCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        