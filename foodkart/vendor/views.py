from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from store.forms import ProductForm
from store.models import Product
from .models import Vendor
from accounts.forms import RegistrationForm, VendorProfileForm, UserForm
from . forms import VendorRegistrationForm, VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile, VendorProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# request.POST, request.FILES, request.POST, request.FILES, 
# Create your views here.
# @login_required
# def vprofile(request):
#     user = request.user
#     up = get_object_or_404(UserProfile, user=user)
#     vp = get_object_or_404(Vendor, vendor=user)
#     if request.method=='POST':
#         vendor_profile = VendorForm(request.POST,instance=vp)
#         user_reg = RegistrationForm(request.POST,instance=user)
#         user_profile = UserProfileForm(request.POST,request.FILES,instance=up)
#         if vendor_profile.is_valid() and user_reg.is_valid() and user_profile.is_valid():
#             vendor_profile.save()
#             user_reg.save()
#             user_profile.save()
#             messages.success(request,'Your Profile has been updated')
#             return redirect('vendorDashboard')
#     else:
#         vendor_profile = VendorForm(instance=vp)
#         user_reg = RegistrationForm(instance=user)
#         user_profile = UserProfileForm(instance=up)
#     context = {
#         'vendor_profile':vendor_profile,
#         'user_reg': user_reg,
#         'user_profile':user_profile,
#         'up':up
#     }
#     return render(request, 'vendor/vprofile.html',context)        
               
    
def vprofile(request):
    user = request.user
    vendor_profile_details = get_object_or_404(VendorProfile, user=user)
    vendor_details = get_object_or_404(Vendor, vendor=user)
    if request.method=='POST':
        vendor_data = VendorForm(request.POST,instance=vendor_details)
        user_reg = UserForm(request.POST,instance=user)
        vendor_profile = VendorProfileForm(request.POST,request.FILES,instance=vendor_profile_details)
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
        vendor_profile = VendorProfileForm(instance=vendor_profile_details)
    context = {
        'vendor_data':vendor_data,
        'user_reg': user_reg,
        'vendor_profile':vendor_profile,
        'vendor_details':vendor_profile_details
    }
    return render(request, 'vendor/vprofile.html',context)



# def vprofile(request):
#     user = request.user
#     vendor=get_object_or_404(Vendor,vendor=user)
#     if request.method == 'GET':
#         vendor_form = VendorRegistrationForm(instance=vendor)
#         user_profile = UserProfile.objects.get(user=user)
#         profile_form = UserProfileForm(instance=user_profile)
#         context={
#                 'vendor':vendor_form,
#                 'profile':profile_form,
#                 'user': user,
#                 'vendor':vendor
#                 }
#         return render(request, 'vendor/vprofile.html', context)
#     else:
#         if request.method == 'POST':
#             user_profile = UserProfile.objects.get(user=user)
#             profile_form = UserProfileForm(request.POST,request.FILES,instance=profile_form)
#             if profile_form.is_valid():
                
#                 profile_form.save()
#                 return redirect('vprofile')
            
        
          
    

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
        