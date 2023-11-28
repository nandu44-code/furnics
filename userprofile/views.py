from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Prefetch
from django.http import Http404, HttpResponse, JsonResponse
from accounts.models import CustomUser, UserWallet
from carts.models import Order, OrderItem
from .models import Address
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from io import BytesIO
from django.conf import settings
from django.db.models import ObjectDoesNotExist

# Create your views here.
def user_profile(request):
    if 'useremail' in request.session:
        email=request.session['useremail']
        user=CustomUser.objects.get(email=email)
        user_id=user.id
        try:
            address=Address.objects.filter(user_id=user_id)
        except:
            address=None
        context={
                'users':user,
                'address':address
            }
    else:
        return redirect('user_login')
    return render(request,'userprofile/user_profile.html',context)

def edit_user_profile(request,user_id):
  
   
    if request.method=='POST':

        user  =CustomUser.objects.get(id=user_id)

        if user:
            
            user.username=request.POST.get('username')
            user.email   =request.POST.get('email')
            user.phone   =request.POST.get('phone')
            user.save()
 
            return redirect('user_profile')

def address_view(request):

    if 'useremail' in request.session:
        email=request.session['useremail']
        user=CustomUser.objects.get(email=email)
        user_id=user.id
        address=Address.objects.filter(user_id=user_id)
        context={
                'users':user,
                'address':address
            }
    else:
        return redirect('user_login')
    return render(request,'userprofile/address.html',context)

def add_address(request,user_id):
    
    if request.method=='POST':
        user=CustomUser.objects.get(pk=user_id)
        user_id=user
        house_no = request.POST.get('house_no')
        recipient_name = request.POST.get('RecipientName')
        street_name = request.POST.get('street_name')
        village_name =  request.POST.get('Village')
        postal_code =  request.POST.get('postal_code')
        district =  request.POST.get('district')
        state =  request.POST.get('state')
        country =  request.POST.get('country')
        exists = Address.objects.filter(user_id=user_id).exists()
        print(exists)
        if exists == False:
        
            address=Address(    
                            user_id = user_id,
                            house_no = house_no,
                            recipient_name = recipient_name,
                            street_name = street_name,
                            village_name =  village_name,
                            postal_code = postal_code,
                            district =  district,
                            state =  state,
                            country =  country,
                            is_default = True
                        )

        else:
             address=Address(
                            user_id = user_id,
                            house_no = house_no,
                            recipient_name = recipient_name,
                            street_name = street_name,
                            village_name =  village_name,
                            postal_code = postal_code,
                            district =  district,
                            state =  state,
                            country =  country,
                            
                        )


        address.save()

        return redirect('user_profile')

def edit_address(request,address_id):
 
    if request.method=='POST':   
        address=Address.objects.get(id=address_id)
        
        address.house_no = request.POST.get('house_no')
        address.recipient_name = request.POST.get('RecipientName')
        address.street_name = request.POST.get('street_name')
        address.village_name =  request.POST.get('Village')
        address.postal_code =  request.POST.get('postal_code')
        address.district =  request.POST.get('district')
        address.state =  request.POST.get('state')
        address.country =  request.POST.get('country')

        address.save()

        return redirect('user_profile')

def delete_address(request,address_id):

    address=Address.objects.get(id=address_id)
    address.delete()
    return redirect('user_profile')



def default_address(request):

    if request.method =='POST':
        try:
            # Attempt to retrieve the default address
            default_address_check = Address.objects.get(is_default=True)
            
            # If a default address exists, remove the old default address
            default_address_check.is_default = False
            default_address_check.save()
            
        except Address.DoesNotExist:
            # Handle the case where no default address exists
            pass

        address_id = request.POST.get("default_address")  # getting the address selected by the user
        
        try:
            # Attempt to retrieve the selected address
            address = Address.objects.get(id=address_id)
            address.is_default = True
            address.save()
        except Address.DoesNotExist:
            # Handle the case where the selected address doesn't exist
            raise Http404("The selected address does not exist")  # Raise Http404 to indicate a not found error

    return redirect('user_profile')

def my_orders(request):
    if request.user:
        order_items=None
        useremail=request.session['useremail']
        print(useremail)
        user=CustomUser.objects.get(email=useremail)
        try:
            order=Order.objects.filter(user=user.id).distinct()
            
            # order_item=OrderItem.objects.filter(order=order)
            order_items = OrderItem.objects.filter(order__user=user.id).distinct().prefetch_related( Prefetch('order', queryset=order)).order_by('-order', 'id').distinct('order')
        except:
            order=None
            order_items=None
        # order_item =order_item.objects.filter(order=order)
        context={
            "order":order,
            "order_items":order_items
        }

        return render(request,"userprofile/my_orders.html",context)
def order_details(request,order_id):
    
    order=Order.objects.get(id=order_id)
    order_items=OrderItem.objects.filter(order=order)
    status=order.status
    
    context={
        "order_items":order_items,
        "order":order,
        "status":status
    }
    return render(request,"userprofile/order_details.html",context)

def order_cancellation(request, order_id):
    order = Order.objects.get(id=order_id)
    user = request.user

    # try:
    #     user_wallet = UserWallet.objects.get(user=user)
    # except ObjectDoesNotExist:
        # If UserWallet doesn't exist, create a new instance
    user_wallet = UserWallet(user=user, amount=0)  # Set default amount here
    user_wallet.save()

    order.status = 'Cancelled'
    order.save()

    if order.payment_mode == "Paid by Razorpay":
        user.wallet += order.total_price
        user_wallet.amount += order.total_price

    user_wallet.transaction = 'credited'
    user.save()
    user_wallet.save()

    order_items = OrderItem.objects.filter(order=order)
    status = order.status
    context = {
        "order_items": order_items,
        "order": order,
        "status": status
    }
    return render(request, "userprofile/order_details.html", context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def pdf_download(request,id):
    order=Order.objects.get(id=id)
    neworderitems=OrderItem.objects.filter(order=order)
    #    cart_items = CartItem.objects.filter(cart=cart,is_active=True).order_by('id')
    total,quantity,tax,discount=0,0,0,0
    for cart_item in neworderitems:
        total += (cart_item.variant.selling_price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    discount =abs(float(total)+float(tax)-order.total_price)
    cont = {
        'order': order,
        'cart_items': neworderitems,
        'total':total,
        'tax':tax,
        'discount':discount
    }
    pdf = render_to_pdf('userprofile/order_invoice.html', cont)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (cont['order'])
        content = "inline; filename='%s'" % (filename)
        # download = request.GET.get("download")
        # if download:
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response
    
def order_return(request,order_id):

    order=Order.objects.get(id=order_id)
    order.status='Return requested'
    order.save()

    order_items=OrderItem.objects.filter(order=order)
    status=order.status
    context={
        "order_items":order_items,
        "order":order,
        "status":status
    }
    return render(request,"userprofile/order_details.html",context)

def user_wallet(request):

    wallet=UserWallet.objects.filter(user=request.user)
    context={
        'wallet':wallet,
    }

    return render(request,'userprofile/wallet.html',context)