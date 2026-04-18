from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Hello, Akanshu ")
    return render(request, 'index.html')

def about(request):
    return HttpResponse("Hello, HOw are you ?")

def contact(request):
    return HttpResponse("Hello., World")

