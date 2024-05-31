"""
Blended VIEWS
"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def index(request):
    return render(request, 'index.html')

def page_not_found(request):
    """
    Page not found Error 404
    """
    return render(request, 'blended_django_app/404.html', status=404)