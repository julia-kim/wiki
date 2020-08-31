from django.shortcuts import render
from markdown2 import Markdown
from . import util


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