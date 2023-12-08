from django.contrib import admin
from .models import Post, User, Fallow,Like
# Register your models here.

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Fallow)
admin.site.register(Like)