from django.shortcuts import render, redirect
from django . http import HttpResponse, JsonResponse
from dine.models import Cart
from dine.context_processor import get_cart_amount
from . forms import OrderForm
from . models import Order, Payment, OrderedFood
import simplejson as json
from . utils import generate_order_number
from django.contrib.auth.decorators import login_required


# VERIFICATION EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

@login_required(login_url='signin') 
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count<=0:
        return redirect ('hotel_list')
    
    total = get_cart_amount(request)['total']
    tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    tax_data = get_cart_amount(request)['tax_dict']
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name= form.cleaned_data['first_name']
            order.last_name= form.cleaned_data['last_name'] 
            order.phone= form.cleaned_data['phone'] 
            order.email= form.cleaned_data['email'] 
            order.address= form.cleaned_data['address'] 
            order.country= form.cleaned_data['country'] 
            order.state= form.cleaned_data['state'] 
            order.city= form.cleaned_data['city'] 
            order.pin_code= form.cleaned_data['pin_code'] 
            order.user = request.user
            order.total = grand_total
            order.total_tax = tax
            order.tax_data = json.dumps(tax_data)
            order.payment_method= request.POST['payment_method']
            order.save()
            order.order_number= generate_order_number(order.id)
            order.save()
            context = {
                'order':order,
                'cart_items':cart_items,
            }
            return render( request, 'orders/place_order.html', context)                      
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')



    
@login_required(login_url='signin') 
def payments(request):
    # CHECK IF THE REQUEST IS AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # STORE THE PAYMENT DETAILS IN PAYMENT MODEL
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        print(order_number, transaction_id, payment_method, status)

        order = Order.objects.get(user=request.user, order_number=order_number)
        order.order_number = order_number
        order.save()

        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method='paypal',
            amount = order.total,
            status=status
        )        
        payment.save()        

        # UPDATE THE ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        order.save()
        
    
        # MOVE CART ITEMS TO THE ORDERED FOOD MODEL

        cart_items= Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food=OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.product = item.product
            ordered_food.quantity = item.quantity
            ordered_food.price = item.product.price
            ordered_food.amount = item.product.price * item.quantity
            ordered_food.save()
            # return HttpResponse('Mail sent')
        
        # SENT ORDER CONFIRAMTION EMAIL TO THE CUSTOMER
        current_site= get_current_site(request)
        mail_subject = "Thankyou for ordering with us"
        message = render_to_string('orders/order_confirmation.html',{
            'order': order,           
        })
        to_email= order.email
        print(to_email,current_site)
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        


        # SENT ORDER RECEIVED MAIL TO THE VENDOR        
        current_site= get_current_site(request)
        mail_subject = "You have received an order"
        message = render_to_string('orders/vendor_order_confirmation.html',{
            'order': order,           
        })
        mail_list=[]
        for i in cart_items:
            if i.product.vendor.vendor.email not in mail_list:
                mail_list.append(i.product.vendor.vendor.email)
        to_email= mail_list        
        print(current_site)
        print(to_email)
        send_email = EmailMessage(mail_subject, message, to=to_email)
        send_email.send()
        

        # CLEAR THE CART IF PAYMENT IS SUCCESS
        # cart_items.delete()
        # RETURN BACK TO AJAX WITH THE STATUS SUCCESS OR FAILURE
        response = {
            'order_number':order_number,
            'transaction_id': transaction_id
        }
        return JsonResponse(response)
    return HttpResponse('Payments_View')
        

def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
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
        return render(request, 'orders/order_complete.html', context)
    except:
        return redirect('home_page')

    


        
         
