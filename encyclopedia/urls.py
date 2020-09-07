from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("<str:title>/edit", views.edit, name="edit"),
    path("random", views.rand, name="random"),
    path("search", views.search, name="search"),
    path("<str:title>", views.entry, name="entry")
]
