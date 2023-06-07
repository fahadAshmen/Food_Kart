from django.db import models
from accounts.models import Account, UserProfile


# Create your models here.
class Vendor(models.Model):
    vendor     =models.OneToOneField(Account, on_delete=models.CASCADE)
    # user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    vendor_name= models.CharField(max_length=100)
    is_vendor  =models.BooleanField(default=False)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    v_profile_pic = models.ImageField(upload_to='vendors/profile_picture',blank=True,null=True)
   
   

    

    def __str__(self):
        return self.vendor_name