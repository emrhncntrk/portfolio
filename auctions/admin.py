from django.contrib import admin
from .models import listings, comments, bids, User, categories
# Register your models here.

admin.site.register(listings)
admin.site.register(comments)
admin.site.register(bids)
admin.site.register(User)
admin.site.register(categories)
