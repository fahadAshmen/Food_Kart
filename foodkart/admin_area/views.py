from decimal import Decimal
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from store.models import Category
from . forms import CategoryForm
from vendor.models import Vendor
from django.contrib import messages
from accounts.models import Account
from django.db.models import Q
from orders.models import Order, Payment, OrderedFood
from foody.models import AdminWallet
import simplejson as json
from vendor.models import VendorWallet
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/accounts/signin/')
def admin_area(request):
    orders=Order.objects.filter(is_ordered=True)
    order_count=orders.count()
    vendor= Vendor.objects.all()          
    vendor_count = vendor.count()
    customers = Account.objects.filter(role="CUSTOMER")
    customers_count=customers.count()
    context={
      'order_count':order_count, 
      'vendor_count':vendor_count,
      'customers_count':customers_count,
    }
    return render(request, 'admin_area/admin_dashboard.html', context)

@login_required(login_url='/accounts/signin/')
def add_category(request):   
    # form = CategoryForm() 
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            description=form.cleaned_data['description']
            category=Category.objects.create(category_name=category_name,description=description,slug=category_name.replace(" ","-").lower())
            category.save()
        else:
            print (form.errors)
        return redirect('admin_area')
    else:
        form=CategoryForm()    
    return render(request, 'admin_area/add_category.html', {'form':form})

@login_required(login_url='/accounts/signin/')
def vendor_list(request):
    vendor= Vendor.objects.all()   
    vendor_count = vendor.count()
    context = {
        'vendors' : vendor,
        'vendor_count': vendor_count,
    }
    return render(request,'admin_area/vendor_list.html', context)


@login_required(login_url='/accounts/signin/')
def block_vendor(request, vendor_id):
    vendor=Vendor.objects.get(id=vendor_id)        
    if vendor.is_approved:
        vendor.is_approved=False
        vendor.save()      
        messages.success(request,"Vendor has been blocked")    
    else:
        vendor.is_approved=True          
        messages.success(request,"Vendor has been unblocked")        
        vendor.save()  
    return redirect('vendor_list')



@login_required(login_url='/accounts/signin/')
def user_list(request):
    users = Account.objects.filter(Q(role="VENDOR") | Q(role="CUSTOMER")).order_by('date_joined')    
    user_count=users.count()
    context={
        'users':users,
        'user_count':user_count,
    }
    return render(request, 'admin_area/user_list.html',context)
#ERROR Account.objects.filter(Q(role='CUSTOMER') | Q(role='VENDOR'))


@login_required(login_url='/accounts/signin/')
def block_user(request, account_id):
    user = Account.objects.get(id=account_id)

    if user.is_active==True:
        user.is_active=False
        messages.success(request,"User has been blocked")
    else:
        user.is_active=True
        messages.success(request,"User has been unblocked")
    user.save()    
    return redirect('user_list')

@login_required(login_url='/accounts/signin/')
def sales_records(request):
    orders=Order.objects.all().order_by('-created_at')
    order_count=orders.count()
    context={
        'orders':orders,
        'order_count':order_count
    }
    return render(request,'admin_area/sales_records.html',context)

@login_required(login_url='/accounts/signin/')
def admin_wallet(request):
    orders=Order.objects.filter(is_ordered=True)
    order_count=orders.count()
    wallet=AdminWallet.objects.all().order_by('-created_at')
    total_trans=0
    total_comm=0
    for t in wallet:
        total_trans=total_trans+ t.trans_amount
        if t.admin_commision:
            total_comm += t.admin_commision
    context = {
        'wallets':wallet,
        'total_trans':total_trans,
        'total_comm':total_comm,
        'order_count':order_count,
    }
    return render(request, 'admin_area/admin_wallet.html',context)

@login_required(login_url='/accounts/signin/')
def make_payment(request, trans_id):
    transaction_details = AdminWallet.objects.get(id=trans_id)

    if transaction_details.payment_status == True:
        messages.success(request,"Payment already done")
        return redirect('admin_wallet')
    else:
        try:
            with transaction.atomic():
                lists=[]
                for vendor in transaction_details.order.vendors.all():
                    lists.append(vendor.id)
                    
                for v_id in lists:
                    total = Decimal(0)
                    tax = Decimal(0)
                    service_charge=Decimal(0)
                    tax_dict = {}
                    grand_total = Decimal(0)
                    vendor = Vendor.objects.get(id=v_id)
                    vendor_wallet= VendorWallet.objects.get(vendor=vendor)
                    for trans in [transaction_details.order]:
                        if trans.total_data and trans.charge_data:
                            total_data = json.loads(trans.total_data)
                            charge_data = json.loads(trans.charge_data)
                            price_data=total_data.get(str(v_id))
                            comm_data=charge_data.get(str(v_id))
                            print(price_data)
                            print(comm_data)

                            for key,val in price_data.items():
                                total += Decimal(key)
                                tax_dict.update(val)

                            #{{CGST : {9:10},{sgst: {9:10}}}
                            
                            for i in tax_dict:
                                for j in tax_dict[i]:
                                    tax += Decimal(tax_dict[i][j])

                            for key,val in comm_data.items():
                                for i in val:
                                    service_charge += Decimal(comm_data[key][i])
                            
                            grand_total = total + tax - service_charge
                            print(v_id,"-",grand_total)

                            transaction_details.trans_amount -= grand_total
                            transaction_details.save()

                            vendor_wallet.balance += grand_total
                            vendor_wallet.save()
                            # return redirect('admin_wallet')

                transaction_details.payment_status=True
                transaction_details.save() 
                messages.success(request,"Payment alloted successfully")
        except Exception as e:
            print(e)
            messages.success(request,"Oops..! Something Went Wrong")           
                
    return redirect('admin_wallet')
    # context={
    #    'trans_id': trans_id,
    # }
    # return render(request, 'admin_area/make_payment.html', context)