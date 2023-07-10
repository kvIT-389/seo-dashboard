from django.http import HttpResponse

from django.shortcuts import render


def index(request: HttpResponse):
    return render(request, "index.html")
