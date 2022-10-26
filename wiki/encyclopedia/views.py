from audioop import reverse
from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util
from django import forms


class SearchEntries(forms.Form):
    searchQuery = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


class NewEntryName(forms.Form):
    newEntryName = forms.CharField(label = 'Entry Name')


class NewEntryContent(forms.Form):
    newEntryContent = forms.CharField(label = 'Entry Info')


def searchResults(request,query):
    if len(util.search(query)) == 0:
        results = False
    else:
        results = True
    return render(request, "encyclopedia/searchResults.html",{
        "searchedPhrase": query,
        "searchMatches": util.search(query),
        "searchEntries": SearchEntries(),
        "results": results
    })

def index(request):
    if request.method == "POST":
        query = SearchEntries(request.POST)
        if query.is_valid():
            query = query.cleaned_data['searchQuery']
            return searchResults(request, query)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchEntries": SearchEntries()
    })


def entry(request, title):
    if request.method == "POST":
        query = SearchEntries(request.POST)
        if query.is_valid():
            query = query.cleaned_data['searchQuery']
            return searchResults(request, query)

    return render(request, "encyclopedia/entry.html", {
        "content": util.get_entry(title),
        "title": title,
        "searchEntries": SearchEntries()
    })
    
def newEntry(request):
    if request.method == 'POST' and "create" in request.POST :
        name = NewEntryName(request.POST)
        content = NewEntryContent(request.POST)
        if name.is_valid() and content.is_valid(): 
            name = name.cleaned_data['newEntryName']
            content = content.cleaned_data['newEntryContent']
            util.save_entry(name,content)
            return HttpResponseRedirect("/")
        else:
            return render(request,"encyclopedia/newEntry.html",{
                'newEntryName': name,
                'newEntryContent':content
            })
    if request.method == "POST":
        query = SearchEntries(request.POST)
        if query.is_valid():
            query = query.cleaned_data['searchQuery']
            return searchResults(request, query)

    return render(request,"encyclopedia/newEntry.html",{
            'newEntryName': NewEntryName(),
            'newEntryContent': NewEntryContent(),
            "searchEntries": SearchEntries()
            })