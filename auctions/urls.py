from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing,name="create_listing"),
    path("<int:listing_id>", views.view_listing,name="view_listing"),
    path("<int:listing_id>/watchlist", views.edit_watchlist,name="edit_watchlist"),
    path("<int:listing_id>/bid", views.bid,name="bid"),
    path("<int:listing_id>/comment", views.comment,name="comment"),
    path("list_watchlist", views.list_watchlist,name="list_watchlist"),
    path("all_categories", views.all_categories,name="all_categories"),
    path("<int:category_id>/category", views.view_category,name="view_category"),
    path("<int:listing_id>/close_listing", views.close_listing,name="close_listing"),
]
