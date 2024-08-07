from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
def index(request):
    """Redirect the user to the application homepage"""
    return redirect("myapp:home")


def home(request):
    """The user homepage, which displays after logging in."""
    return HttpResponse("placeholder")

