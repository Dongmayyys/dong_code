from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


class NewTaskForm(forms.Form):
    task = forms.CharField(label="new task:")


def index(request):
    if request.session.get("tasks") == None:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session['tasks']
    })


def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            print(type(request.session.get('tasks')))
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    else:
        return render(request, "tasks/add.html", {
            "form": NewTaskForm()
        })
