from django.urls import path
from . import views

urlpatterns = [
    # CRUD OPERATIONS  
    path('addProduct/',views.addProduct,name='addProduct'),
    path('addProduct/<int:id>/',views.addProduct,name='productUpdate'),
    path('viewProduct/', views.product_view, name='view_product'),
    path('deleteProduct/<int:id>/',views.deleteProduct,name='deleteProduct'),

    path('vprofile/',views.vprofile,name='vprofile'),
    
    path('opening_hour/',views.opening_hour, name='opening_hour'),
    path('opening_hour/add/',views.add_opening_hour, name='add_opening_hour'),
    path('opening_hour/remove/<int:pk>/',views.remove_opening_hour, name='remove_opening_hour'),

    path('order_details/<int:order_number>',views.order_details, name='vendor_order_details'),
    path('vendor-orders/',views.vendor_orders,name='vendor_orders'),

]
