from django.db import models
from accounts.models import Account


# Create your models here.
class Vendor(models.Model):
    vendor     =models.OneToOneField(Account, on_delete=models.CASCADE)
    vendor_name= models.CharField(max_length=100)
    is_vendor  =models.BooleanField(default=False)

    

    def __str__(self):
        return self.vendor_name