from django.db import models
from django.contrib.auth.models import User

#Model for adding or removing a stock to a user portfolio
class Add(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="userAdding")
    stock = models.CharField(max_length=16) 

    def __str__ (self):
        return f"{self.user} has added {self.stock} to their portfolio."
    
#Models for storing a list of currency or future symbols so that it can be edited by an admin
class Currency(models.Model):
    symbol= models.CharField(max_length=16)
    
    def __str__ (self):
        return self.symbol
    
class Future(models.Model):
    symbol= models.CharField(max_length=16)
    
    def __str__ (self):
        return self.symbol