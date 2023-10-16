from django.db import models
from accounts.models import Account, UserProfile
from accounts.utils import send_notification
from datetime import time, datetime, date


# Create your models here.
class Vendor(models.Model):
    vendor     =models.OneToOneField(Account, on_delete=models.CASCADE)
    vendor_name= models.CharField(max_length=100)
    # is_vendor  =models.BooleanField(default=False)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    # v_profile_pic = models.ImageField(upload_to='vendors/profile_picture',blank=True,null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.vendor_name
    
    
    #@property
    def is_open(self):
        today_date=date.today()
        today= today_date.isoweekday()
    
        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')

        
        is_open=None
        for hour in current_opening_hours:
            start = str(datetime.strptime(hour.from_hour, '%I:%M %p').time())
            end = str(datetime.strptime(hour.to_hour, '%I:%M %p').time())
            if current_time > start and current_time < end:
                is_open = True
                break
            else:
                is_open=False
        return is_open
            
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            #Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template= 'accounts/emails/vendor_approval_mail.html'
                context = {
                    'vendor' :self.vendor,
                    'is_approved' : self.is_approved,
                    'orig': orig
                }
                if self.is_approved == True:
                    mail_subject = "Congratulations! Your restaurant has been approved"                    
                    send_notification(mail_subject, mail_template, context)
                    #SEND NOTIFICATION MAIL
                else:
                    #SEND NOTIFICATION MAIL
                    mail_subject = "We are sorry! Your restaurant has not been approved to be listed on Foody. Please contact our team for any queries"
                    send_notification(mail_subject, mail_template, context)
                    
        return super(Vendor, self).save(*args, **kwargs)
    
class VendorWallet(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name='wallet_obj', blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
     
    def __str__(self):
       return str(self.vendor)

    
DAYS=[
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

HOUR_OF_DAY = [(time(h,m).strftime('%I:%M %p'), time(h,m).strftime('%I:%M %p')) for h in range(0,24) for m in (0,30)]


class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour=models.CharField(choices=HOUR_OF_DAY, max_length=12, blank=True)
    to_hour=models.CharField(choices=HOUR_OF_DAY, max_length=12, blank=True)
    is_closed=models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('vendor','day', 'from_hour', 'to_hour')
        

    def __str__(self):
        return self.get_day_display()