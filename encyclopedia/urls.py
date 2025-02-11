from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/create/", views.create_entry, name="create_entry"),
    path("wiki/random/", views.random_page, name="random_page"),
    path("wiki/<str:title>/", views.title, name="title"),
    path("wiki/<str:title>/edit/",views.edit_entry, name="edit_entry"), 
]
