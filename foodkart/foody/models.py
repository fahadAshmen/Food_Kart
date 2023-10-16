from django.db import models
from orders.models import Payment, Order
from vendor.models import Vendor

# Create your models here.

class AdminWallet(models.Model):
    transaction = models.ForeignKey(Payment,on_delete=models.CASCADE,max_length=25,blank=True,null=True)
    trans_amount = models.IntegerField()
    order= models.ForeignKey(Order, on_delete=models.CASCADE, null=True,blank=True,related_name="admins_order_details")
    admin_commision=models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
    created_at= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    payment_status=models.BooleanField(max_length=10,null=True,blank=True,default=False)
    # vendors=models.ManyToManyField(Vendor,blank=True,null=True,through="Vendors_In_Trans")

        
    def __str__(self):
        return str(self.transaction)

# class TransactionDetails(models.Model):
#      transaction_details=models.ForeignKey(AdminWallet,on_delete=models.CASCADE, related_name="transaction_details")

class TransactionDetails(models.Model):
    pass




class Charges(models.Model):
    charge_type=models.CharField(max_length=15,unique=True)
    charge_percentage=models.DecimalField(max_digits=4,decimal_places=2)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.charge_type
    
    class Meta:
        verbose_name_plural= 'Charges'



