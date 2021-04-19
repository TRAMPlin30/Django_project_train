from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    name = 'Bob Li Sweger'
    return render(request, 'home.html', {'name':name})

def about(request):
    name = 'Lorem Ipsum ... text '
    return render(request, 'about.html', {'name':name})