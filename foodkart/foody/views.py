from django.shortcuts import render
from store.models import Product
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin import site
from . models import TransactionDetails

# Create your views here.


def home(request):
    product = Product.objects.filter(is_available=True)[:4]
    context = {
        'products':product
    }
    return render(request,'foody/home.html',context)
  

def custom_change_list_view(request, model_admin):    
    return render(request, 'admin/yourapp/yourmodel/custom_change_list.html')


