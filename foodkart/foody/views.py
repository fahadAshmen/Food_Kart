from django.shortcuts import render
from store.models import Product

# Create your views here.


def home(request):
    product = Product.objects.filter(is_available=True)[:4]
    context = {
        'products':product
    }
    return render(request,'foody/home.html',context)

