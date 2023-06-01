from django.urls import path
from . import views

urlpatterns = [
    # path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),   
    path('addProduct/',views.addProduct,name='addProduct'),
    path('addProduct/<int:id>/',views.addProduct,name='productUpdate'),
    path('viewProduct/', views.product_view, name='view_product'),
    path('deleteProduct/<int:id>/',views.deleteProduct,name='deleteProduct'),
]
