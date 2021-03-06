from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from markdown2 import Markdown
from . import util
import random


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "titleinput",
                "placeholder": "Title goes here",
            }
        ),
    )
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "textarea",
                "placeholder": "Enter the content of your article here.",
            }
        ),
    )

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if util.get_entry(title):
            entries = util.list_entries()
            for entry in entries:
                if title.lower() == entry.lower():
                    title = entry
            msg = format_html(
                f"<em>There is already an article named <a href='{title}'>{title}</a></em>.",
                reverse("wiki:entry", args=(title,)),
            )
            self.add_error("title", msg)
        return title


class EditEntryForm(forms.Form):
    prefix = "edit"
    content = forms.CharField(
        initial="md",
        label="",
        widget=forms.Textarea(attrs={"class": "textarea"}),
    )


class SearchForm(forms.Form):
    q = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "search"}),
    )


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "total": len(util.list_entries())},
    )


def entry(request, title):
    if util.get_entry(title):
        md = Markdown().convert(util.get_entry(title))
        entries = util.list_entries()
        for entry in entries:
            if title.lower() == entry.lower():
                title = entry
        return render(
            request, "encyclopedia/entry.html", {"title": title, "content": md}
        )
    else:
        return render(request, "encyclopedia/error.html")


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = f"#{title}" + "\n\n" + form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:entry", args=(title,)))

    else:
        form = NewEntryForm()

    return render(request, "encyclopedia/create.html", {"form": form})


def edit(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html")

    elif request.method == "POST":
        edit_form = EditEntryForm(request.POST)
        if edit_form.is_valid():
            content = edit_form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:entry", args=(title,)))

    else:
        edit_form = EditEntryForm(initial={"content": util.get_entry(title)})

    return render(
        request, "encyclopedia/edit.html", {"title": title, "form": edit_form}
    )


def rand(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse("wiki:entry", args=(entry,)))


def search(request):
    query = request.GET.get("q", False)
    entries = util.list_entries()
    results = []
    isValidQuery = False
    for entry in entries:
        if query and (not query.isspace()):
            isValidQuery = True
            if query.lower() == entry.lower():
                return HttpResponseRedirect(reverse("wiki:entry", args=(entry,)))
            elif query.lower() in entry.lower():
                results.append(entry)
    return render(
        request,
        "encyclopedia/search.html",
        {
            "form": SearchForm(),
            "query": query,
            "results": results,
            "isValidQuery": isValidQuery,
        },
    )
