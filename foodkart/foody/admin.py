from django.contrib import admin
from . models import AdminWallet, Charges, TransactionDetails
from django.contrib.admin.views.main import ChangeList
# from .views import transaction_details
from .views import custom_change_list_view



class ChargesAdmin(admin.ModelAdmin):
    list_display = ['charge_type','charge_percentage','is_active']


    
class CustomAdminWallet(admin.ModelAdmin):
    list_display = ['transaction', 'order', 'admin_commision', 'trans_amount','payment_status']

   

class CustomTransactionDetails(admin.ModelAdmin):
    change_list_template = 'admin/foody/TransactionDetails/change_list.html'
    
    def changelist_view(self, request, extra_context=None):
        # Add additional context variables here
        custom_context = {
            'extra_data': 'Fahad',
        }
        if extra_context is not None:
            extra_context.update(custom_context)
        else:
            extra_context = custom_context
        return super().changelist_view(request, extra_context=extra_context)

# class TransactionDetailsAdmin(admin.ModelAdmin):
#     def changelist_view(self, request, extra_context=None):
#         return custom_change_list_view(request, self)



admin.site.register(TransactionDetails, CustomTransactionDetails)
admin.site.register(AdminWallet, CustomAdminWallet)
admin.site.register(Charges, ChargesAdmin)


# class CustomAdminWallet(admin.ModelAdmin):    
#     list_display = ['transaction','order','admin_commision','trans_amount']
#     # change_list_template = 'foody/admin/change_list.html'
#     def changelist_view(self, request, extra_context=None):
#         if self.model == AdminWallet:
#             self.list_template = 'admin/adminwallet_change_list.html'
#         return super().changelist_view(request, extra_context)


# def changelist_view(self, request, extra_context=None):
#     if self.model == AdminWallet:
#         self.change_list_template = 'admin/adminwallet_change_list.html'
#     return super().changelist_view(request, extra_context)