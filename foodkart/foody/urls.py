from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.home,name='home_page'),
   # path('transactiondetails/',views.transaction_details,name='transaction_details')

]#transactiondetails/

# admin.site.site_header = "Foody Admin"
# admin.site.site_title = "Foody Admin Portal"
# admin.site.index_title = "Welcome to Foody Admin Portal"

# # Make sure you include this line to include the app's URLs in the admin
# admin.autodiscover()
# admin.site.register_view('transactiondetails/', view=transaction_details, name='transaction_details')
