from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content = models.CharField(max_length=256)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
                                                                #Timestamp
        return f"{self.user} has posted {self.id} on {self.date.strftime('%m/%d/%Y, %H:%M')}"
    
    #function to get the amount of likes of a post
    def like_count(self):
        return self.postLiked.count()
    
class Fallow(models.Model):
    fallowing = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fallowing")
    fallowed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fallowed")

    def __str__(self):

        return f"{self.fallowing} fallows: {self.fallowed}."
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLiking")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postLiked")

    def __str__(self):

        return f"{self.user} liked: {self.post}."