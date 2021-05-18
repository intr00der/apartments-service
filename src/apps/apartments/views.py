from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    return render(request, 'apartments/home.html')
