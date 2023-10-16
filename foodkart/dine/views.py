from django.shortcuts import render, get_object_or_404, redirect
from . models import Cart
from accounts.models import VendorProfile
from . context_processor import get_cart_counter, get_cart_amount
from vendor.models import Vendor, OpeningHour
from store.models import Category, Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm
from accounts.models import UserProfile
from django.db.models import Count


from datetime import date, datetime



# Create your views here.

def hotel_list(request):    
    vendor = Vendor.objects.annotate(product_count=Count("product")).filter(is_approved=True, vendor__is_active=True,product_count__gt=0) #.values("vendor_name","product_count")
    # vendor = Vendor.objects.filter(is_approved=True, vendor__is_active=True)
    vendors_count = vendor.count()
    print(vendors_count)    
    context = {
        'vendors': vendor,
        'vendors_count':vendors_count
    }
    return render(request,"dine/dine.html", context)


#VENDOR MENU DETAILS
def vendor_details(request, vendor_slug):
    # vendor = Vendor.objects.annotate(product_count=Count("product")).filter(is_approved=True, vendor__is_active=True,product_count__gt=0).values("vendor_name","product_count")
    vendor=get_object_or_404(Vendor, vendor_slug=vendor_slug)    
    product = Product.objects.filter(vendor=vendor)
    print(product)
    opening_hour = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')

    #get current day opening hour
    today_date=date.today()
    today= today_date.isoweekday()
    
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)
   
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items=None
    context={
        'vendor':vendor,
        'products': product,
        'cart_items':cart_items,
        'opening_hour':opening_hour,
        'current_opening_hours' : current_opening_hours        
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
                    return JsonResponse({'status':'Success','message':'Increased the cart quantity', 'cart_counter' : get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)})                                
                except:
                    chkCart=Cart.objects.create(user=request.user,product=product,quantity=1)
                    return JsonResponse({'status':'Success','message':'Added the product to the cart', 'cart_counter' : get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)})
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
                    return JsonResponse({'status':'Success', 'cart_counter' : get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)})                                
                except:                    
                    return JsonResponse({'status':'Failed','message':'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status':'Failed','message':'This product does not exists'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})           
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    
    
  
@login_required(login_url='/accounts/signin/') 
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    # closed_cart_items_ids=Cart.objects.filter(user=request.user,product__vendor_is_open=True)
    context={
        'cart_items':cart_items
    }
    return render(request, 'dine/cart.html',context)




def delete_cart(request, cart_id):    
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # ==================Check if cart item exists===============
                cart_item=Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message':'Cart item has been deleted','cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amount(request)})
                
            except:
                return JsonResponse({'status':'Failed','message':'Cart item does not exist'})         
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})      
        
        

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count<=0:
        return redirect ('hotel_list')
    user_profile = UserProfile.objects.get(user=request.user)
    default_values={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
        
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items':cart_items
    }
    return render(request, 'dine/checkout.html', context)     
        

      