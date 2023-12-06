from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class categories(models.Model):
    categories = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.categories}"
    


class listings(models.Model):   
    lister = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    min_bid = models.IntegerField()
    image= models.CharField(max_length=256, blank=True)
    category = models.ForeignKey(categories, on_delete=models.CASCADE,null=True, blank=True,related_name="get_category")
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User,default="NULL", null=True, blank=True, related_name= "watchlisting")
    def __str__(self):
        return f"{self.lister} listed {self.title}: {self.description} {self.min_bid} {self.image} {self.category} {self.watchlist}"
    
class bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    product= models.ForeignKey(listings, null=True, on_delete=models.CASCADE, related_name="get_bid")
    
    def __str__(self):
        return f"{self.amount}"    
    
    
class comments(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text= models.TextField(max_length=256)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE, related_name="get_comment") 

    def __str__(self):
        return f"{self.commentor}: {self.comment_text}"
    


    
