from django.shortcuts import render


def index(request):
    return render(request, "auth/index.html")


def login(request):
    return render(request, "auth/login.html")
