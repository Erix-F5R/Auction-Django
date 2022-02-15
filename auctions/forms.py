from django import forms
from .models import Auction, Bid, Comment



class NewListingForm(forms.ModelForm):
    
    #title = forms.CharField(max_length= 120)
    #text = forms.CharField()
    #url = forms.URLField()
    #category = forms.ChoiceField(choices=Auction.CATEGORIES)
    #min_bid = forms.DecimalField()
    

    class Meta:
        model = Auction
        fields = ['title', 'text', 'category', 'url', 'min_bid']
        