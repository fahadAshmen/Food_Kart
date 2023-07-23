from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Account, UserProfile, VendorProfile
from django.utils.html import format_html
# Register your models here.



class CustomAdmin(UserAdmin):
    
    list_display = ['email', 'username','first_name','last_name', 'role','last_login','date_joined','is_active']
    list_display_links= ('email', 'username','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = []
    list_filter = []
    fieldsets = []

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.profile_picture:  # Check if profile picture exists
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(obj.profile_picture.url))
        else:
            return 'No Image'  # Display a default message or placeholder image
        
    thumbnail.short_description = "Profile Picture"
    list_display = ['thumbnail','user','address','country','state','city']


#VENDOR PROFILE   
class VendorProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.profile_picture:  # Check if profile picture exists
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(obj.profile_picture.url))
        else:
            return 'No Image'  # Display a default message or placeholder image
    
    def get_vendor_name(self, obj):
        if obj.user.vendor.vendor_name:
            return obj.user.vendor.vendor_name
        else:
            return 'No Vendor'
    
       
    thumbnail.short_description = "Profile Picture"
    get_vendor_name.short_description = "Vendor Name"
    
    list_display = ['thumbnail','get_vendor_name','user','address','country','state','city']

admin.site.register(Account, CustomAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(VendorProfile, VendorProfileAdmin)