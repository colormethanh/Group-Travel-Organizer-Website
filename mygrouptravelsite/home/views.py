from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def HomePage(request):
    html = "<html><body>Welcome to my front page!</body></html>"
    return HttpResponse(html)
