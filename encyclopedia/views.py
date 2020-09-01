from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Enter title")
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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