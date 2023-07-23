from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import UserProfile, Account
from accounts.forms import UserForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderedFood
import simplejson as json


@login_required(login_url='/accounts/signin/')
def custProfile(request):
    user=request.user
    print(user)
    user_profile_details = get_object_or_404(UserProfile, user=user)
    print('==>',user_profile_details)
    if request.method == 'POST':
        user_reg= UserForm(request.POST,instance=user)
        user_profile = UserProfileForm(request.POST, request.FILES,instance=user_profile_details)
        if user_reg.is_valid() and user_profile.is_valid():
            user_reg.save()
            user_profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('custProfile')
        else:
            user_reg_errors = user_reg.errors.as_data()
            user_profile_errors = user_profile.errors.as_data()
            errors = []            
            errors.extend(user_reg_errors)
            errors.extend(user_profile_errors)
            for error in errors:
                messages.error(request, error)
            return redirect('custProfile')
    else:
        user_reg= UserForm(instance=user)
        user_profile = UserProfileForm(instance=user_profile_details)

    form = {
        'user_reg' : user_reg,
        'user_profile' : user_profile,
        'user_profile_details' : user_profile_details
    }
    return render(request, 'customer/custProfile.html', form) 

@login_required(login_url='/accounts/signin/')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user)
        print(user)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully")
                return redirect('custDashboard')
            else:
                messages.error(request,"Please enter valid current password")
                return redirect('change_password')
        else:
            messages.error(request, "Password does not match")
            return redirect('change_password')
    return render(request, 'customer/change_password.html')

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    orders_count = orders.count()    
    context={
        'orders' : orders,
        'orders_count' : orders_count,        
    }
    return render(request, 'customer/my_orders.html', context)

def order_details(request, order_number):
    print(order_number)    
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food=OrderedFood.objects.filter(order=order)

        total = 0
        for item in ordered_food:
            total+= (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        print(tax_data)
        context={
            'order': order,
            'ordered_food':ordered_food,
            'total': total,
            'tax_data':tax_data
        }
        return render(request, 'customer/order_details.html', context)
    except:
        return redirect('home_page')
    

