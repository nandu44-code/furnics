from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from accounts.models import CustomUser, UserWallet
from django.contrib import messages
from categories.models import Category,Sub_Category
from carts.models import Order,OrderItem
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.template.loader import get_template
from xhtml2pdf import pisa
from dashboard.models import Banner
from store.models import Coupon, Product, Variation
# Create your views here.
# view function for admin login
def admin_login(request):
    if 'adminemail' in request.session:
        return redirect('admin_home')

    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        user=authenticate(request,email=email,password=password)
        if user is not None and user.is_superuser:
            login(request,user)
            request.session['adminemail']=email
            return redirect('admin_home')
        else:
            messages.error(request,"invalid credentials try again!!!")

            

    return render(request,'dashboard/adminlogin.html')



def adminhome(request):
    total_sales = 0
    if request.method == 'POST':
        users=CustomUser.objects.filter(is_active=True).count()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        print(start_date)
        request.session['start_date'] = start_date
        request.session['end_date'] = end_date

        # date_obj = datetime.strptime(start_date, '%d-%m-%Y')
        # date_obj2 = datetime.strptime(end_date, '%d-%m-%Y')

        # Convert the datetime object to a string in yyyy-mm-dd format
        # start_date = date_obj.strftime('%Y-%m-%d')
        # end_date = date_obj2.strftime('%Y-%m-%d')

        if start_date == end_date:
            print(start_date)
            orders = Order.objects.filter(created_at__date=start_date)
        else:
            orders = Order.objects.filter(created_at__range=(start_date, end_date))
        total_order = Order.objects.filter(created_at__range=(start_date, end_date)).count()
        Pending = Order.objects.filter(created_at__range=(start_date, end_date),status='Order confirmed').count()
        Processing = Order.objects.filter(created_at__range=(start_date, end_date),status="In Production").count()
        Shipped = Order.objects.filter(created_at__range=(start_date, end_date),status='Shipped').count()
        Delivered = Order.objects.filter(created_at__range=(start_date, end_date),status='Delivered').count()
        cancelled = Order.objects.filter(created_at__range=(start_date, end_date),status='Cancelled').count()
        Return = Order.objects.filter(created_at__range=(start_date, end_date),status='Returned').count()

        for order in orders:
            total_sales = total_sales + order.total_price
            
        context = {
                "users":users,
                # 'total':total,
                'orders': orders,
                'total_sales': total_sales,
                'total_order': total_order,
                'Pending': Pending,
                'Processing': Processing,
                'Shipped': Shipped,
                "Delivered": Delivered,
                'cancelled': cancelled,
                'Return': Return,
                "sales":Delivered,
                "cancelled":cancelled,
                # "returned":returned,
                # 'monthly_sales_data': monthly_sales_data
            }
        return render(request, 'dashboard/adminhome.html', context)

    else:

        orders = Order.objects.all()
        total_order = Order.objects.all().count()
        Pending = Order.objects.filter(status='Order confirmed').count()
        Processing = Order.objects.filter(status="In Production").count()
        Shipped = Order.objects.filter(status='Shipped').count()
        Delivered = Order.objects.filter(status='Delivered').count()
        cancelled = Order.objects.filter(status='Cancelled').count()
        Return = Order.objects.filter(status='Returned').count()
        for order in orders:
            total_sales = total_sales + order.total_price
        
        if 'adminemail' in request.session:

            current_year = timezone.now().year

            # Calculate monthly sales for the current year
            monthly_sales = Order.objects.filter(
                created_at__year=current_year
            ).annotate(month=ExtractMonth('created_at')).values('month').annotate(total_sales=Sum('total_price')).order_by(
                'month')

            # Create a dictionary to hold the monthly sales data
            monthly_sales_data = {month: 0 for month in range(1, 13)}

            for entry in monthly_sales:
                month = entry['month']
                total_sales = entry['total_sales']
                monthly_sales_data[month] = total_sales
            users=CustomUser.objects.all().count()
            try:

                sales=Order.objects.filter(status="Delivered").count()
                revenue=Order.objects.filter(status="Delivered")
                total=0
                for i in revenue:
                    total+=i.total_price
            except:
                sales=0
            try:

                cancelled=Order.objects.filter(status="Cancelled").count()
            except:
                cancelled=0
            try:

                returned=Order.objects.filter(status="Returned").count()
            except:
                returned=0

            context = {
                "users":users,
                'total':total,
                'orders': orders,
                'total_sales': total_sales,
                'total_order': total_order,
                'Pending': Pending,
                'Processing': Processing,
                'Shipped': Shipped,
                "Delivered": Delivered,
                'cancelled': cancelled,
                'Return': Return,
                "sales":sales,
                "cancelled":cancelled,
                "returned":returned,
                'monthly_sales_data': monthly_sales_data
            }
            return render(request, 'dashboard/adminhome.html', context)
        else:
            return redirect('admin_login')

    # if 'adminemail' in request.session:

    #     current_year = timezone.now().year

    #     # Calculate monthly sales for the current year
    #     monthly_sales = Order.objects.filter(
    #         created_at__year=current_year
    #     ).annotate(month=ExtractMonth('created_at')).values('month').annotate(total_sales=Sum('total_price')).order_by(
    #         'month')

    #     # Create a dictionary to hold the monthly sales data
    #     monthly_sales_data = {month: 0 for month in range(1, 13)}

    #     for entry in monthly_sales:
    #         month = entry['month']
    #         total_sales = entry['total_sales']
    #         monthly_sales_data[month] = total_sales
    #     users=CustomUser.objects.all().count()
    #     try:

    #         sales=Order.objects.filter(status="Delivered").count()
    #     except:
    #         sales=0
    #     try:

    #         cancelled=Order.objects.filter(status="Cancelled").count()
    #     except:
    #         cancelled=0
    #     try:

    #         returned=Order.objects.filter(status="Returned").count()
    #     except:
    #         returned=0
        # context={
        #     "sales":sales,
        #     "cancelled":cancelled,
        #     "returned":returned,
        #     'monthly_sales_data': monthly_sales_data
        # }
        # return render(request,'dashboard/adminhome.html',context)
    # else:
    #     return redirect('admin_login')


def adminlogout(request):

    if 'adminemail' in request.session:

        logout(request)
        request.session.flush()
        return redirect('admin_login')
    else:
        return redirect('admin_login')
    

# view function for going to users page
def users(request):
    if 'adminemail' in request.session:
        user=CustomUser.objects.filter(is_superuser=False).order_by('id')
    
        context={
             'users':user
                }
        return render (request,'dashboard/users.html',context)

    else:
        return redirect('admin_login')
 

# view function for blocking and unblocking the user
def block_user(request,user_id):
    
    user=CustomUser.objects.get(pk=user_id)

    if user.is_active:
        user.is_active=False
        user.save()
        if request.session['useremail']:
            del request.session['useremail']
        users=CustomUser.objects.filter(is_superuser=False).order_by('id')
    
        context={
                'users':users
        }

        return render(request,'dashboard/users.html',context)
    else:
        user.is_active=True
        user.save()
        users=CustomUser.objects.filter(is_superuser=False).order_by('id')
    
        context={
                'users':users
        }

        return render(request,'dashboard/users.html',context)
    

def categories(request):
    if 'adminemail' in request.session:
        category=Category.objects.all().order_by('id')
        context={
            'categories':category
        }

        return render(request,'dashboard/categories.html',context)
    else:
        return redirect('admin_login')

def add_categories(request):

    if request.method=="POST":
        category_name=request.POST.get('categoryName')
        category_desc=request.POST.get('categoryDescription')
        category_image = request.FILES.get('category_img')
        
        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request,"Entered Category is already taken!!")
            return redirect('categories')
            
        else:
            category=Category(category_name=category_name,description=category_desc,category_image=category_image)
            category.save()
            return redirect('categories')
    # return render(request,'dashboard/users.html')

def edit_categories(request,category_id):
    category = Category.objects.get(id=category_id)
    category_image=category.category_image
    if request.method=="POST":
        category_name= request.POST.get('categoryName')
        
        category.description    = request.POST.get('categoryDescription')
        category_img = request.FILES.get('category_img')

        if category_img is None:
            category.category_image = category_image
    
        else:
            category.category_image = category_img

        if Category.objects.filter(category_name=category_name).exclude(id=category_id).exists():
            messages.error(request,"Entered Category is already taken!!")
            return redirect('categories')
            
        else:
             category.category_name  = category_name
             category.save()
             return redirect('categories')
    # return render(request,'dashboard/users.html')

def delete_categories(request,category_id):
    category=Category.objects.get(pk=category_id)

    if category.is_activate:
        category.is_activate=False
        category.save()
        try:
            sub=Sub_Category.objects.filter(category=category)
            for item in sub:
                item.is_activate=False
                item.save()
                try:
                    products=Product.objects.filter(sub_category=item)
                    for product in products:
                        product.is_activate=False
                        print('hihterehhtereerereerererere')
                        try:
                            variant=Variation.objects.filter(product=product)
                            for variant in variant:
                                variant.is_available=False
                        except:
                            pass
                except:
                    pass
        except:
            pass
       
    
        category=Category.objects.all().order_by('id')
        context={
            'categories':category
        }
        return render(request,'dashboard/categories.html',context)
    else:
        category.is_activate=True
        category.save()
        # categories=Category.objects.all
        try:
            sub=Sub_Category.objects.filter(category=category)
            for item in sub:
                item.is_activate=True
                item.save()
                try:
                    products=Product.objects.filter(sub_category=item)
                    for product in products:
                        product.is_activate=True
                        try:
                            variant=Variation.objects.filter(product=product)
                            for variant in variant:
                                variant.is_available=True
                        except:
                            pass
                except:
                    pass
        except:
            pass

        category=Category.objects.all().order_by('id')
        context={
            'categories':category
        }
        return render(request,'dashboard/categories.html',context)


def sub_categories(request):
    category=Category.objects.filter(is_activate=True)
    subcategory=Sub_Category.objects.all().order_by('id')
    context={
        'subcategories':subcategory,
        'categories':category
    }

    return render(request,'dashboard/subcategories.html',context)
 
def add_subcategories(request):
    if request.method=="POST":
         # setting value as category_name as category id and fetching it 
        category_id=request.POST.get('category_name')
        # using category id update the category field of sub_category by passing the particular category instance
        category_instance = Category.objects.get(pk=category_id)
        sub_category_name=request.POST.get('categoryName')
        description = request.POST.get('categoryDescription')
        cat_image = request.FILES.get('cat_img')
        cat = Sub_Category(category=category_instance, sub_category_name=sub_category_name, sub_category_description=description,
                           sub_Category_image=cat_image)
        cat.save()   
        return redirect('sub_categories')
        
def edit_subcategories(request,subcategory_id):

    subcategory=Sub_Category.objects.get(pk=subcategory_id)
    # fetching the image from data base for when user is not edited the image field we will have to give the previous image  
    sub_category_image=subcategory.sub_Category_image

    if request.method=="POST":
        # setting value as category_name as category id and fetching it 
        category_id = request.POST.get('category_name')
        # using category id update the category field of sub_category
        subcategory.category = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get('categoryName')
        subcategory.sub_category_name =  sub_category_name
        subcategory.sub_category_description = request.POST.get('categoryDescription')

        sub_Category_img = request.FILES.get('cat_img')
        # checking if the subcategory image is none 
        if sub_Category_img is None:
            subcategory.sub_Category_image = sub_category_image
        else:
            subcategory.sub_Category_image = sub_Category_img      


        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exclude(id=subcategory_id).exists():

            messages.error(request,"Entered Sub Category is already taken!!")
            return redirect('sub_categories')
        
        else:

            subcategory.save()   
            return redirect('sub_categories')
            
def delete_subcategories(request,subcategory_id):

    category=Sub_Category.objects.get(pk=subcategory_id)

    if category.is_activate:
        category.is_activate=False
        category.save()

       
        
        category=Category.objects.filter(is_activate=True).order_by('id')
        subcategory=Sub_Category.objects.all().order_by('id')
        context={
            'subcategories':subcategory,
            'categories':category
        }

        return render(request,'dashboard/subcategories.html',context)
    else:
        category.is_activate=True
        category.save()
        

        category=Category.objects.filter(is_activate=True).order_by('id')
        subcategory=Sub_Category.objects.all().order_by('id')
        context={
            'subcategories':subcategory,
            'categories':category
         }
    return render(request,'dashboard/subcategories.html',context)


def orders(request):

    orders = Order.objects.all()
    order_items = OrderItem.objects.order_by('order').distinct('order')
    for i in order_items:
        print(i.quantity)
    context={
        "orders":orders,
        "orderitems":order_items
    }
    return render(request,"dashboard/orders.html",context)

def orders_details(request,order_id):
    
    order=Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)

    context={
        "order":order,
        "orderitems":order_item
    }

    return render(request,"dashboard/orders_details.html",context)


def order_status(request):
  
    if request.method == 'POST':
        url = request.META.get('HTTP_REFERER')
        try:
            order_id = request.POST.get('order_id')
            order_status = request.POST.get('order_status')
            print(order_status)
            if order_status == 'Order Status':
                order = Order.objects.get(id=order_id)
                order_item = OrderItem.objects.filter(order=order)
                context = {
                    'order': order,
                    'order_item': order_item
                }
                return redirect(url)
                # return render(request, 'dashboard/orders_details.html', context)
            order = Order.objects.get(id=order_id)
            order_item = OrderItem.objects.filter(order=order)
            
            order.status = order_status
            order.save()
            if order_status == 'Returned':
                email = order.user.email
                user = CustomUser.objects.get(email=email)
                user.wallet = user.wallet + order.total_price
                userwallet = UserWallet()
                userwallet.user = user
                userwallet.amount = order.total_price
                userwallet.transaction = 'Credited'
                userwallet.save()
                user.save()
            order_item = OrderItem.objects.filter(order=order)
            context = {
                'order': order,
                'order_item': order_item
            }
            print(order.total_price)
            print("order_status")
            return redirect(url)
         
        except:
            pass
    print("order_status")
    order_item = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_item': order_item
    }
    return render(request, 'dashboard/orders_details.html', context)

def get_sales_revenue(request):
    # Replace this with your actual data retrieval logic
    # Example mock data
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'sales': [100, 200, 150, 300, 250, 400],
        'revenue': [500, 600, 550, 700, 650, 800],
    }

    return JsonResponse(data)




def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Sales_report.pdf"'

    # Create a PDF with xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sales_report_pdf_download(request):
    if 'start_date' and 'end_date' in request.session:
         start_date = request.session['start_date']
         end_date = request.session['end_date']
         try:
             order = Order.objects.filter(created_at__range=(start_date, end_date))
             del request.session['start_date']
             del request.session['end_date']
         except:
             order=None
    else:

        order = Order.objects.all()
    cont = {
        'orders': order,
    }
    pdf = render_to_pdf('dashboard/sales_report_pdf.html', cont)
    return pdf

def coupon(request):
    
    coupon=Coupon.objects.all().order_by('id')

    context={
        'coupon':coupon,
    }
    return render(request,'dashboard/coupons.html',context)

def add_coupon(request):
    
    if request.method=='POST':
        coupon_name=request.POST.get('couponName')
        coupon_code=request.POST.get('couponCode')
        discountAmount=request.POST.get('discountAmount')
        validFrom=request.POST.get('validFrom')
        validTo=request.POST.get('validTo')
        minimumAmount=request.POST.get('minimumAmount')

        if Coupon.objects.filter(coupon_name=coupon_name).exists():
            messages.error(request,"Entered Coupon is already exists!!")
            return redirect('coupon')
        elif Coupon.objects.filter(code=coupon_code).exists():
            messages.error(request,"Entered Coupon code is already exists!!")
            return redirect('coupon')
            
        else:
            coupon=Coupon(coupon_name=coupon_name,code=coupon_code,discount=discountAmount, valid_from = validFrom, valid_to = validTo, minimum_amount = minimumAmount)
            coupon.save()

            return redirect('coupon')
        
def edit_coupon(request,coupon_id):

    if request.method=='POST':
        coupon=Coupon.objects.get(id=coupon_id)

        coupon_name = request.POST.get('couponName')
        coupon.coupon_name = coupon_name

        coupon_code = request.POST.get('couponCode')
        coupon.coupon_code = request.POST.get('couponCode')

        coupon.discount = request.POST.get('discountAmount')
        coupon.valid_from = request.POST.get('validFrom')
        coupon.valid_to = request.POST.get('validTo')
        coupon.minimum_amount = request.POST.get('minimumAmount')

        

        if Coupon.objects.filter(coupon_name=coupon_name).exclude(id=coupon_id).exists():

            messages.error(request,"Coupon name you have chosen is already taken ")
            return redirect('coupon')
        
        elif Coupon.objects.filter(code=coupon_code).exclude(id=coupon_id).exists():
             messages.error(request,"Coupon code you have chosen is already taken ")
             return redirect('coupon')
        
        else:
            coupon.save()
            return redirect('coupon')
        
def block_coupon(request,coupon_id):

    coupon=Coupon.objects.get(id=coupon_id)
    print("hjksjhfkjhdkjfhksjdfhksdhfksdjhfksjdhk")
    if coupon.is_available == True:
        
        coupon.is_available=False
    else:
        coupon.is_available=True
    coupon.save()
    return redirect('coupon')


def banner(request):
    banner=Banner.objects.all()

    context={
        'banner':banner,
    }

    return render(request,'dashboard/banner.html',context)

def add_banner(request):
    if request.method=='POST':
        banner_name = request.POST.get('bannername')
        banner_image = request.FILES.get('banner_img')

        try:
            banner_records_count = Banner.objects.count()
        
        except:
            banner_records_count=0
        
       
      
        if banner_records_count<1:

            if Banner.objects.filter(banner_name=banner_name).exists():
                messages.error(request,"Entered banner name is already taken!!")
                return redirect('banner')
                
            else:
                banner=Banner(banner_name= banner_name,banner_image=banner_image)
                banner.save()
                return redirect('banner')
        else:
            messages.error(request,"banner limit is reached!!")
            return redirect('banner')
        
def edit_banner(request,banner_id):

    banner = Banner.objects.get(id=banner_id)
    banner_image = banner.banner_image
    if request.method=="POST":
        banner_name= request.POST.get('bannername')
        
        banner_images = request.FILES.get('banner_img')

        if banner_images is None:
            banner.banner_image = banner_image
    
        else:
            banner.banner_image = banner_images

        if Banner.objects.filter(banner_name=banner_name).exclude(id=banner_id).exists():
            messages.error(request,"Entered Banner name is already taken!!")
            return redirect('banner')
            
        else:
             banner.banner_name  = banner_name
             banner.save()
             return redirect('banner')

def remove_banner(request,banner_id):

    banner=Banner.objects.get(id=banner_id)
    
    banner.delete()


    return redirect('banner')