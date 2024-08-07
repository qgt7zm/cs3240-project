from django.http import HttpResponse


def root(request):
    """Redirect the user to the main app"""
    return HttpResponse("placeholder")
