from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from orders.models import Order, OrderedFood
from store.forms import ProductForm
from store.models import Product
from .models import Vendor, OpeningHour
from accounts.forms import UserForm
from . forms import VendorForm, OpeningHourForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from urllib import response



def get_vendor(request):
    vendor = Vendor.objects.get(vendor=request.user)
    return vendor
   
    
def vprofile(request):
    user = request.user
    vendor_profile_details = get_object_or_404(UserProfile, user=user)
    vendor_details = get_object_or_404(Vendor, vendor=user)
    if request.method=='POST':
        vendor_data = VendorForm(request.POST,instance=vendor_details)
        user_reg = UserForm(request.POST,instance=user)
        vendor_profile = UserProfileForm(request.POST,request.FILES,instance=vendor_profile_details)
        if vendor_data.is_valid() and user_reg.is_valid() and vendor_profile.is_valid():
            vendor = vendor_data.save(commit=False)  # Create vendor object without saving
            vendor.vendor = request.user  # Assign the vendor field
            vendor.save()  # Save the vendor object  
               
            user_reg.save()
            vendor_profile.save()
            messages.success(request,'Your Profile has been updated')
            return redirect('vprofile')
        else:
            vendor_errors = vendor_profile.errors.as_data()
            user_reg_errors = user_reg.errors.as_data()
            user_profile_errors = user_profile.errors.as_data()
            errors = []
            errors.extend(vendor_errors)
            errors.extend(user_reg_errors)
            errors.extend(user_profile_errors)
            for error in errors:
                messages.error(request, error)
            return redirect('vprofile')
    else:
        vendor_data = VendorForm(instance=vendor_details)
        user_reg = UserForm(instance=user)
        vendor_profile = UserProfileForm(instance=vendor_profile_details)
    context = {
        'vendor_data':vendor_data,
        'user_reg': user_reg,
        'vendor_profile':vendor_profile,
        'vendor_details':vendor_profile_details
    }
    return render(request, 'vendor/vprofile.html',context)

    
# def vprofile(request):
#     user = request.user
#     vendor_profile_details = get_object_or_404(VendorProfile, user=user)
#     vendor_details = get_object_or_404(Vendor, vendor=user)
#     if request.method=='POST':
#         vendor_data = VendorForm(request.POST,instance=vendor_details)
#         user_reg = UserForm(request.POST,instance=user)
#         vendor_profile = VendorProfileForm(request.POST,request.FILES,instance=vendor_profile_details)
#         if vendor_data.is_valid() and user_reg.is_valid() and vendor_profile.is_valid():
#             vendor = vendor_data.save(commit=False)  # Create vendor object without saving
#             vendor.vendor = request.user  # Assign the vendor field
#             vendor.save()  # Save the vendor object  
               
#             user_reg.save()
#             vendor_profile.save()
#             messages.success(request,'Your Profile has been updated')
#             return redirect('vprofile')
#         else:
#             vendor_errors = vendor_profile.errors.as_data()
#             user_reg_errors = user_reg.errors.as_data()
#             user_profile_errors = user_profile.errors.as_data()
#             errors = []
#             errors.extend(vendor_errors)
#             errors.extend(user_reg_errors)
#             errors.extend(user_profile_errors)
#             for error in errors:
#                 messages.error(request, error)
#             return redirect('vprofile')
#     else:
#         vendor_data = VendorForm(instance=vendor_details)
#         user_reg = UserForm(instance=user)
#         vendor_profile = VendorProfileForm(instance=vendor_profile_details)
#     context = {
#         'vendor_data':vendor_data,
#         'user_reg': user_reg,
#         'vendor_profile':vendor_profile,
#         'vendor_details':vendor_profile_details
#     }
#     return render(request, 'vendor/vprofile.html',context)



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

def opening_hour(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form':form,
        'opening_hours':opening_hours
    }
    return render(request, 'vendor/hour.html', context)

def add_opening_hour(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            print(day,from_hour,to_hour,is_closed)
            try:
                hour=OpeningHour.objects.create(vendor=get_vendor(request),day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status': 'success', 'id':hour.id, 'day':day.get_day_display(), 'is_closed': 'Closed'}
                    else:
                        response = {'status': 'success', 'id':hour.id, 'day':day.get_day_display(), 'from_hour':hour.from_hour, 'to_hour': hour.to_hour}                
                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status':'Failed', 'message': from_hour+' - '+to_hour+' already exists for this day'}
                return JsonResponse(response)
        else:
            return HttpResponse('Invalid request')
        

def remove_opening_hour(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour=get_object_or_404(OpeningHour, pk=pk)
            print('==>',hour)
            hour.delete()
            return JsonResponse({'status':'success', 'id': pk})
        
def order_details(request, order_number):    
    try:
        orders = Order.objects.get(order_number=order_number, is_ordered = True)
        ordered_food = OrderedFood.objects.filter(order=orders, product__vendor=get_vendor(request))        
        context ={
            'order' : orders,
            'ordered_food' : ordered_food,
            'total' : orders.get_total_by_vendor()['total'],
            'tax_data' : orders.get_total_by_vendor()['tax_dict'],
            'grand_total' : orders.get_total_by_vendor()['grand_total'],         
         }
        return render (request, 'vendor/order_details.html', context)
    except:
        return redirect('vendorDashboard')


          
        