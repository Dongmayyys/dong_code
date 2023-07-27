from django.shortcuts import render
from datetime import datetime
# Create your views here.


def index(request):
    now = datetime.now()
    flag = True
    if now.month == 7 and now.day == 27:
        flag = False
    return render(request, "newyear/isitnewyear.html", {
        "flag": flag,
    })
