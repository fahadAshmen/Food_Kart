from django.shortcuts import render, redirect
from store.forms import ProductForm
from store.models import Product
from django.http import HttpResponse
from .models import Vendor



# Create your views here.


# def addProduct(request, id=0):
#     form = ProductForm()
#     if request.method == 'POST':
#         if id==0:
#             form = ProductForm(request.POST, request.FILES)
#         else:
#             product=Product.objects.get(pk=id)
#             form = ProductForm(request.POST, request.FILES, instance=product)
#             if form.is_valid():
#                 product = form.save(commit=False)
#                 product.vendor = request.user.vendor
#                 print(product.vendor)
#                 product.save()
#                 return redirect('view_product') 
#     else:
#         if request.method == 'GET':
#             if id==0:
#                 form = ProductForm()
#             else:
#                 product=Product.objects.get(pk=id)
#                 form=ProductForm(request.POST, request.FILES, instance=product)         
#                 return render(request,'vendor/addProduct.html',{'form':form})

def addProduct(request, id=0):
    form = ProductForm()
    if request.method== 'GET':
        if id==0:
            form = ProductForm()
        else:
            product = Product.objects.get(pk=id)
            form = ProductForm(instance=product)        
        return render(request, 'vendor/addProduct.html', {'form': form})
    else:
        if request.method == 'POST':
            if id==0:
                form = ProductForm(request.POST, request.FILES)
            else:
                product = Product.objects.get(pk=id)
                form = ProductForm(request.POST,request.FILES, instance=product)                        
            if form.is_valid():
                product = form.save(commit=False)
                product.vendor = request.user.vendor
                print(product.vendor)
                product.save()
                return redirect('view_product')
        
def product_view(request):
    user = request.user
    vendor = Vendor.objects.get(vendor=user)
    product = Product.objects.filter(vendor=vendor)    
    return render(request, 'vendor/viewProduct.html', {'products': product})

def deleteProduct(request, id):
    product = Product.objects.get(pk=id)
    product.delete()
    return redirect('view_product')
        