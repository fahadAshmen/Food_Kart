from django.shortcuts import render, get_object_or_404
# from store.models import Product
from accounts.models import VendorProfile
from vendor.models import Vendor
from store.models import Category, Product



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

def vendor_details(request, vendor_slug):
    vendor=get_object_or_404(Vendor, vendor_slug=vendor_slug)
    
    product = Product.objects.filter(vendor=vendor)
    context={
        # 'vendors': [vendor],
        'products': product,
        }
    return render(request, 'dine/vendor_details.html', context)
