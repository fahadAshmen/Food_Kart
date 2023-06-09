from django.shortcuts import render, get_object_or_404, HttpResponse
from . models import Cart
from accounts.models import VendorProfile
from . context_processor import get_cart_counter
from vendor.models import Vendor
from store.models import Category, Product
from django.http import JsonResponse



# Create your views here.

def hotel_list(request):
    # vendor_profile = VendorProfile.objects.filter()
    vendor = Vendor.objects.filter(is_vendor=True, vendor__is_active=True)
    vendors_count = vendor.count()
    print(vendor)
    context = {
        'vendors': vendor,
        'vendors_count':vendors_count
    }
    return render(request,"dine/dinedemo.html", context)


#VENDOR MENU DETAILS
def vendor_details(request, vendor_slug):
    vendor=get_object_or_404(Vendor, vendor_slug=vendor_slug)
    
    product = Product.objects.filter(vendor=vendor)
    
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items=None
    context={
        'products': product,
        'cart_items':cart_items
        }
    return render(request, 'dine/vendor_details.html', context)
# 'vendors': [vendor],



# ADD TO CART
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if the product exists
            try:
                product=Product.objects.get(id=product_id)
                #check if the user has already added the product to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user,product=product)
                    chkCart.quantity +=1
                    chkCart.save()
                    return JsonResponse({'status':'Success','message':'Increased the cart quantity', 'cart_counter' : get_cart_counter(request), 'qty': chkCart.quantity})                                
                except:
                    chkCart=Cart.objects.create(user=request.user,product=product,quantity=1)
                    return JsonResponse({'status':'Success','message':'Added the product to the cart', 'cart_counter' : get_cart_counter(request), 'qty': chkCart.quantity})
            except:
                return JsonResponse({'status':'Failed','message':'This product does not exists'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})           
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    
    
def decrease_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if the product exists
            try:
                product=Product.objects.get(id=product_id)
                #check if the user has already added the product to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user,product=product)
                    if chkCart.quantity >1:
                        #decrease the cart quantity
                        chkCart.quantity -=1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status':'Success', 'cart_counter' : get_cart_counter(request), 'qty': chkCart.quantity})                                
                except:                    
                    return JsonResponse({'status':'Failed','message':'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status':'Failed','message':'This product does not exists'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})           
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    
    
    
# def decrease_cart(request, product_id):
#     if request.user.is_authenticated:
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             #Check if the product exists
#             try:
#                 product=Product.objects.get(id=product_id)
#                 #check if the user has already added the product to the cart
#                 try:
#                     chkCart = Cart.objects.get(user=request.user,product=product)
#                     if chkCart.quantity >1:
#                         #decrease the cart quantity
#                         chkCart.quantity -=1
#                         chkCart.save()
#                     else:
#                         chkCart.delete()
#                         chkCart.quantity = 0
#                         return JsonResponse({'status':'Success', 'cart_counter' : get_cart_counter(request), 'qty': chkCart.quantity})                                
#                 except:                    
#                     return JsonResponse({'status':'Failed','message':'You do not have this item in your cart!'})
#             except:
#                 return JsonResponse({'status':'Failed','message':'This product does not exists'})
#         else:
#             return JsonResponse({'status':'Failed','message':'Invalid request'})           
#     else:
#         return JsonResponse({'status':'Failed','message':'Please login to continue'})