from django.urls import path
from . import views

urlpatterns=[
    path('',views.admin_area,name='admin_area'),
    path('add_category/',views.add_category,name='add_category'),
    path('vendor_list/',views.vendor_list,name='vendor_list'),
    path('block-vendor/<int:vendor_id>',views.block_vendor,name="block_vendor"),
    path('user_list/',views.user_list,name="user_list"),
    path('block-user/<int:account_id>/',views.block_user,name='block_user'),
    path('sales-records/',views.sales_records,name='sales_records'),
    path('admin-wallet/',views.admin_wallet,name='admin_wallet'),
    path('make_payment/<int:trans_id>/',views.make_payment,name='make_payment'),

]