
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("makePost", views.makePost, name="makePost"),
    path("user/<str:username>", views.userProfile, name="profile"),
    path("fallowing", views.fallowing, name="fallowing"),
    path("fallowUser", views.fallowUser, name="fallowUser"),
    path("posts/<int:post_id>", views.editPost, name="editPost"),
    path("like/<str:action>/<int:post_id>", views.likePost, name="likePost")
       
]
