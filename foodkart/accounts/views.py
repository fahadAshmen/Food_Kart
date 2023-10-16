import datetime
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from . forms import RegistrationForm
from . models import Account, UserProfile, VendorProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from . utils import check_role_customer, check_role_vendor
# from django.http import HttpResponseRedirect

from vendor.models import Vendor, VendorWallet
from vendor.forms import VendorRegistrationForm
from django.template.defaultfilters import slugify

from orders.models import Order

# VERIFICATION EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

#USER REGISTRATION
def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.role= 'CUSTOMER'
            user.phone_number=phone_number
            user.save()
            UserProfile.objects.create(user=user)
            #USER ACTIVATION
            current_site= get_current_site(request)           
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/email_verification.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email= email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request,'Thankyou for registering with us. We have sent a verification mail. Please verify it.')
            return redirect('signin')
            # return redirect('signin/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
       'form':form,
    }
   
    return render(request,'accounts/userRegister.html', context)


def signin(request):
    if request.user.is_authenticated:
         return redirect('home_page')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                # Redirect to the 'next' URL specified in the POST data
                return redirect(request.POST['next'])            
            elif user.role == 'VENDOR' and request.user.vendor.is_approved:
                return redirect('vendorDashboard')
            elif user.role =='CUSTOMER':
                return redirect('custDashboard')
            elif user.role == None and request.user.is_admin:
               return redirect('/admin_area/')
            # elif user.role == None and request.user.is_superadmin:
            #     return redirect('/admin/')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('signin')
    return render(request, 'accounts/signin.html')



#LOGIN
# def signin(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['password']
#         print(email, password)
#         user = authenticate(email=email,password=password)
#         print(user)
#         if user is not None:
#             login(request, user)
#             if user.role == 'VENDOR' and request.user.vendor.is_approved:
#                 return redirect('vendorDashboard')                        
#                 # return render(request, 'vendor/vendorDashboard.html')

#             elif user.role =='CUSTOMER':
#                 return redirect('custDashboard')
                
#             else: 
#                  return redirect('/admin/')
                 
#         # else:
#         #     return redirect('home_page')
                 
#             # messages.success(request,"You are logged in")
#             # return redirect('home_page')
#         else:
#             messages.error(request,'Invalid login credentials')
#             return redirect('signin')
#     return render(request, 'accounts/signin.html')

#LOGOUT
@login_required(login_url='/accounts/signin/')
def signout(request):
    logout(request)
    messages.success(request,"You are logged out")
    return redirect('signin')
    #HttpResponseRedirect


def dashboard(request):
     user=request.user
     if user.is_authenticated:
        if user.role == 'VENDOR' and user.vendor.is_approved:
            return redirect('vendorDashboard')
        elif user.role =='CUSTOMER':
            return redirect('custDashboard')
        elif user.role == None and request.user.is_admin:
               return redirect('/admin_area/')
                
     else:
          return redirect('home')




#USER ACTIVATION LINK
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request,"Congratulations!, Your account is activated")
            return redirect("signin")
    else:
            messages.error(request,"Invalid activation link")
            return redirect('user_register')

#FORGOT PASSWORD
def forgotPassword(request):
     if request.method == 'POST':
          email = request.POST['email']
          if Account.objects.filter(email=email).exists():
               user = Account.objects.get(email__exact=email)

               #Reset Password email
               current_site= get_current_site(request)
               mail_subject = "Reset Your Password"
               message = render_to_string('accounts/resetPasswordEmail.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
               })
               to_email= email
               send_email = EmailMessage(mail_subject, message, to=[to_email])
               send_email.send()

               messages.success(request, 'Password reset email has been sent to your mail address.')
               return redirect('signin')
          else:
               messages.error(request,'Account does not exist')
               return redirect('forgotPassword')                      

     return render(request, 'accounts/forgotPassword.html')

#RESET PASSWORD LINK 
def resetpassword_validate(request, uidb64, token):
     try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
     except(TypeError, ValueError,OverflowError, Account.DoesNotExist):    
        user = None

     if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request,"Please reset your password")
            return redirect('resetPassword')
     else:
            messages.error(request,"The link has been expired")
            return redirect('signin')
     

#RESETTING PASSWORD
def resetPassword(request):
     if request.method=="POST":
          password = request.POST['password']
          confirm_password = request.POST['confirm_password']

          if password == confirm_password:
               uid = request.session.get('uid')
               user= Account.objects.get(pk=uid)
               user.set_password(password)
               user.save()
               messages.success(request, 'Password reset successful')
               return redirect('signin')             

          else:
               messages.error(request,"Password do not match")
               return redirect('resetPassword') 
     else:
          return render(request, 'accounts/resetPassword.html')  
     
#VENDOR REGISTRATION
def register_vendor(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            username = email.split("@")[0]
            user = Account.objects.create_user(email=email,first_name=first_name,last_name=last_name,password=password,username=username)
            user.role= 'VENDOR'
            user.phone_number=phone_number
            user.save()
            UserProfile.objects.create(user=user)            
            
            #USER ACTIVATION
            current_site= get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/email_verification.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email= email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #VENDOR ACTIVATION
            vendor_name=form.cleaned_data['vendor_name']
            vendor = Vendor.objects.create(vendor=user,
                vendor_name=form.cleaned_data['vendor_name'])
                # is_vendor=False)
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            vendor.save()
            VendorWallet.objects.create(vendor=vendor)            
            
            return redirect('signin')

    else:
        form = VendorRegistrationForm()
    context = {
       'form':form,
    }
   
    return render(request,'accounts/vendor_register.html', context)

      
#VENDOR DASHBOARD
@login_required(login_url='/accounts/signin/')
@user_passes_test(check_role_vendor)
def vendorDashboard(request): 
    
    vendors = Vendor.objects.get(vendor=request.user)
    vendor_wallet= VendorWallet.objects.get(vendor=vendors)
    for vendor in [vendors]:
        pass
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')
    recent_orders = orders[:5]

    #monthly_revenue
    current_month = datetime.datetime.now().month
    current_month_orders =orders.filter(vendors__in=[vendor.id], created_at__month=current_month)
    current_month_revenue=0
    for i in current_month_orders:
         if i.get_total_by_vendor():
              current_month_revenue += i.get_total_by_vendor()['grand_total']    
    
    #total_revenue
    total_revenue=0
    for i in orders:
         if i.get_total_by_vendor():
              total_revenue += i.get_total_by_vendor()['grand_total']
    


    
    context = {
         'orders' : orders,
         'orders_count' : orders.count(),
         'recent_orders' : recent_orders,
         'total_revenue' : total_revenue,
         'current_month_revenue' : current_month_revenue,
         'vendor_wallet':vendor_wallet,
    }

    return render(request, 'vendor/vendorDashboard.html', context)
    # return render(request, 'vendor/vendorDashboard.html')
    
#CUSTOMER DASHBOARD
@login_required(login_url='/accounts/signin/')
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    orders_count = orders.count()
    recent_orders = orders[:5]
    context={
        'orders' : orders,
        'orders_count' : orders_count,
        'recent_orders' : recent_orders
    }
    return render(request, 'customer/custDashboard.html', context)




