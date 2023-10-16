from django.contrib import admin
from . models import Vendor, OpeningHour,VendorWallet

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    
    list_display=['vendor_name','is_approved','vendor']
    list_editable=['is_approved',]  

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'day', 'from_hour', 'to_hour']  

class CustomVendorWallet(admin.ModelAdmin):
    list_display=['vendor','balance']

admin.site.register(Vendor, VendorAdmin)
admin.site.register(VendorWallet, CustomVendorWallet)
admin.site.register(OpeningHour, OpeningHourAdmin)

