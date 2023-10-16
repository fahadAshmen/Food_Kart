from django.db import models
from accounts.models import Account
from store.models import Product
from vendor.models import Vendor
import simplejson as json

# Create your models here.

request_object= ''


class Payment(models.Model):    
    PAYMENT_METHOD = (
        ('PayPal', 'Paypal'),
        ('Razorpay', 'Razorpay')
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id= models.CharField(max_length=20)
    payment_method=models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status= models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction_id
    
class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=20)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15, blank=True)
    email=models.EmailField(max_length=50)
    address=models.CharField(max_length=200)
    country=models.CharField(max_length=15, blank=True)
    state=models.CharField(max_length=15, blank=True)
    city=models.CharField(max_length=50)
    pin_code=models.CharField(max_length=10)
    total=models.FloatField()
    tax_data=models.JSONField(blank=True, help_text = "Data format:{'tax_type':{'tax_percentage':'tax_amount'}}", null=True)
    total_data = models.JSONField(blank=True, null=True)
    charge_data=models.JSONField(blank=True, null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status=models.CharField(choices=STATUS, max_length=15, default='New')
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def display_vendor(self):
        return ", ".join([str(i) for i in self.vendors.all()])
    
    


    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(vendor=request_object.user)
        if self.total_data and self.charge_data:            
            total_data = json.loads(self.total_data)
            data = total_data.get(str(vendor.id))
            charge_data= json.loads(str(self.charge_data))           
            service_charges=charge_data.get(str(vendor.id))
            
            
            total = 0
            tax = 0
            service_charge=0
            tax_dict = {}
            grand_total = 0
            for key, val in data.items():
                total +=float(key)
                tax_dict.update(val)

                for key,values in service_charges.items():
                    for i in values:
                        service_charge += float(service_charges[key][i])

                
                # calculate tax
                # {'CGST': {'9.00' : '5.00'}, 'SGST': {'9.00' : '5.00'}}
                # {'CGST': {'9.00': '19.80'}, 'SGST': {'9.00': '19.80'}, 'Service Charge': {'10.00': '22.00'}}
                for i in tax_dict:
                    for j in tax_dict[i]:
                        tax += float(tax_dict[i][j])

                # print('1',total)
                # print('2',tax)
                # print('3',service_charge)
            grand_total = float(total) + float(tax) - float(service_charge)
            # print(type(service_charges))
            context ={
                'total': total,
                'tax' : tax,
                'tax_dict' : tax_dict,
                'grand_total': grand_total,
                'service_charges': service_charges,                
            }     
            return context


    
    def __str__(self):
        return self.order_number
    
    
class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.food_title
    
    