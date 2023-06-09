
from django.urls import path
from . import views

urlpatterns = [
    path('',views.hotel_list,name="hotel_list"),
    path('<slug:vendor_slug>/',views.vendor_details,name='vendor_details'),
    
    
    #ADD TO CART
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    #DECREASE CART
    path('decrease_cart/<int:product_id>/',views.decrease_cart,name='decrease_cart'),

] 
