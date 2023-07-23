
from django.urls import path
from . import views

urlpatterns = [
    path('customer-profile',views.custProfile,name="custProfile"),
    path('change-password/',views.change_password,name='change_password'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('order_details/<int:order_number>/',views.order_details,name='order_details'),
] 
