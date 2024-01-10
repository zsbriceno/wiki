from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new-entry", views.new_entry, name="new_entry"),
    path("edit-entry/<str:title>", views.edit_entry, name="edit_entry"),
    path("random-page", views.random_page, name="random_page")
]
