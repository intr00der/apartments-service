from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def home_view(request):
    return render(request, 'apartments/home.html')
