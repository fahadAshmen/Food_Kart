
from django.urls import path
from . import views

urlpatterns = [
    path('',views.hotel_list,name="hotel_list"),
    path('<slug:vendor_slug>/',views.vendor_details,name='vendor_details')
] 
