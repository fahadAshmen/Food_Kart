from django.shortcuts import render, HttpResponse
from django.http import HttpResponse


# Create your views here.

def hotel_list(request):
    return render(request,"dine/hotel.html")
