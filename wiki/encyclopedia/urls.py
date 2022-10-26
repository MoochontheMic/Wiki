from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/newentry", views.newEntry, name = "newEntry" ),  
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/searchresults", views.searchResults, name = "searchResults")
    ]
    
