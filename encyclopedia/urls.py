from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry_page, name="entry_page"),
    path("search_query/", views.search_query, name="search_query"),
    path("create_page/", views.create_page, name="create_page"),
    path("edit_page/", views.edit_page, name="edit_page"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("random_page/", views.random_page, name="random_page"),
    ]
