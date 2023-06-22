from django.contrib import admin
from . models import Payment, Order, OrderedFood

class OderedFoodInline(admin.TabularInline):
    model=OrderedFood
    readonly_fields = ['order','payment','user','product','quantity','price','amount']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','name','phone','email','total','payment_method','status','is_ordered']
    inlines = [OderedFoodInline]



admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)
