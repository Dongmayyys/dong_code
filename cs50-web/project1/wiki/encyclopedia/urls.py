from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("notfound", views.notFound, name="notfound"),
    path("edit", views.edit, name="edit"),
    path("lucky", views.lucky, name="lucky"),
]
