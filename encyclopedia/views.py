from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from . import util
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Enter title")
    content = forms.CharField(widget=forms.Textarea)

class SearchForm(forms.Form): 
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'advanced-search'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "total": len(util.list_entries())
    })

def entry(request, title):
    md = Markdown().convert(util.get_entry(title))
    if util.get_entry(title): 
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": md
        })
    else: 
        return render(request, "encyclopedia/error.html")

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    
    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })

def rand(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=(entry,)))

def search(request):
    query = request.GET['q']
    entries = util.list_entries()
    results = []
    for entry in entries:
        if query.lower() == entry.lower():
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(entry,)))
        if query.lower() in entry.lower():
            results.append(entry)
    return render(request, "encyclopedia/search.html", {
        "form": SearchForm(),
        "query": query,
        "results": results
    })