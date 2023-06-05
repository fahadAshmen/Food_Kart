from django.shortcuts import render
from store.models import Product



# Create your views here.

def hotel_list(request):
    product = Product.objects.filter(is_available=True)
    context ={
        'products' : product
    }
    return render(request,"dine/hotel.html", context)
