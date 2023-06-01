from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class CustomManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,          
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password=password,
            first_name = first_name,
            last_name = last_name,                 
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name   =models.CharField(max_length=50,null=True,blank=True)
    last_name    =models.CharField(max_length=50,null=True,blank=True)
    username     =models.CharField(max_length=50,unique=True)
    email        =models.EmailField(max_length=100,unique=True)
    phone_number =models.CharField(max_length=50)
    
    date_joined  =models.DateTimeField(auto_now_add=True)
    last_login   =models.DateTimeField(auto_now_add=True)
    is_admin     =models.BooleanField(default=False)
    is_staff     =models.BooleanField(default=False)
    is_active    =models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    is_vendor    =models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = CustomManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

# class UserProfile(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE, blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
#     address = models.CharField(max_length=250, blank=True, null=True)
#     country = models.CharField(max_length=15, blank=True, null=True)
#     state = models.CharField(max_length=15, blank=True, null=True)
#     city = models.CharField(max_length=15, blank=True, null=True)
#     pin_code = models.CharField(max_length=10, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
    
    ### def full_address(self):
    ###     return f'{self.address_line_1}, {self.address_line_2}'
    
    
    # def __str__(self):
    #     return self.user.email
    
    