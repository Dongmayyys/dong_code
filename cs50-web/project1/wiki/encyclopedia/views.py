from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
import markdown
from . import util


class CreateForm(forms.Form):
    title = forms.CharField(label="title", widget=forms.TextInput())
    content = forms.CharField(label="content", widget=forms.Textarea())
    test = forms.IntegerField(label="test", max_value=2)


def index(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    if query:
        if query in entries:
            return redirect(reverse("entry", kwargs={"title": query}))
        else:
            entries = [entry for entry in entries if query.lower()
                       in entry.lower()]
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown.markdown(content)
        })
    else:
        return redirect(reverse("notfound"))


def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data["title"] in (entry for entry in util.list_entries()):
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": "used title!"
                })
            else:
                util.save_entry(data["title"], data["content"])
                return redirect(reverse("entry", kwargs={"title": data["title"]}))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    else:
        form = CreateForm()
        return render(request, "encyclopedia/create.html", {
            "form": form
        })


def notFound(request):
    return render(request, "encyclopedia/not_found.html")
