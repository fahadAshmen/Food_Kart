from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.user_register,name='user_register'),
    path('register/signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),

    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),
    path('custDashboard/',views.custDashboard,name='custDashboard'),

    path('activate/<uidb64>/<token>',views.activate,name='activate'), #account activation link

    path('forgotPassword',views.forgotPassword,name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name='resetpassword_validate'), #password activation mail
    path('resetPassword/',views.resetPassword,name='resetPassword'),

    path('registerVendor/',views.register_vendor,name='vendor_register'),
    path('vendor_activate/<vidb64>/<token>',views.vendor_activate,name='vendor_activate'),   #VENDOR ACTIVATION LINK

    # path('registerVendor/',views.vendor_register,name='vendor_register'),

]
