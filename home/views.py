from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.db.models import Q,Max
from categories.models import Category
from categories.models import Sub_Category
from accounts.models import CustomUser
from dashboard.models import Banner
from store.models import Product, Variation

# Create your views here.
@never_cache  
def homepage(request):

   
    
    if 'adminemail' in request.session:
        return redirect('admin_home')
    if request.user:
        user=request.user

    banner=Banner.objects.all()

    context={
        'banner':banner
    }
    return render(request,'home/index.html',context)

def view_shop(request):
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    variants = Variation.objects.filter(is_available=True).order_by('product').distinct('product')
    sub_categories = None

    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()
    context={
        'category':categories,
        'product':products,
        'variants':variants,
        "color":available_colors,
        'sub_categories':sub_categories
    }



    return render(request,'home/shop.html',context)

def view_subcategory(request,category_id):
    variants={}
    subcategory=Sub_Category.objects.filter(Q(is_activate=True) & Q(category=category_id))
    # Assuming you already have 'subcategory' containing the filtered subcategories
    variants = Variation.objects.filter(product__sub_category__in=subcategory,is_available=True)


    context={
        'subcategory':subcategory,
        'base_variant':variants
    }

    return render(request,'home/subcategory.html',context)

def display_products(request,sub_category_id):
    
    subcategory = Sub_Category.objects.get(id=sub_category_id)

    
    variants = Variation.objects.filter(product__sub_category=subcategory,is_available=True)
    
    

    context={
        'variants':variants
            
            }                            

    return render(request,'home/products_display.html',context)

def product_details(request,variant_id):

    variants = Variation.objects.get(pk=variant_id)
    product_id = variants.product

    available_variants =Variation.objects.filter(product=product_id,is_available=True)

    for i in available_variants:

        print(i.color)
    context={
        # 'product':product,
        'variant': variants,
        'available_variants':available_variants
    }

    return render(request,'home/product_details.html',context)

def variant_select(request,variant_id):

    variants = Variation.objects.get(pk=variant_id)
    product_id = variants.product

    return redirect('product_details',variant_id)
    # available_variants =Variation.objects.filter(product=product_id,is_available=True)
    
    # variant_id=variants.id
    # variant_price = variants.selling_price
    # variant_stock = variants.stock
    # variant_image1 = variants.image1.url
    # variant_image2 = variants.image2.url
    # variant_image3 = variants.image3.url
    # variant_image4 = variants.image4.url
    # variant_id = variants.id
        # 'available_vatiants':available_variants
    

    # return JsonResponse({'variant':variant_price,
    #                      'variant_stock':variant_stock,
    #                      'variant_image1':variant_image1,
    #                      'variant_image2':variant_image2,
    #                      'variant_image3':variant_image3,
    #                      'variant_image4':variant_image4,
    #                      'variant_id':variant_id
    #                      })


# def product_search(request):

#     query=request.GET.get('q')
#     modified_string = query.replace(" ", "")
#     variants=None
    
#     categories=Category.objects.filter(is_activate=True)
#     products=Product.objects.filter(is_activate=True)
#     available_colors = Variation.objects.filter(is_available=True).values('color').distinct()
#     if modified_string == "":
        
#         return redirect('shop_page')
    
#     else:

#         product=Product.objects.filter(product_name__icontains=query)
#         for product in product:
            

#             variants=Variation.objects.filter(product=product,is_available=True)
#         print(variants)
#         context={
#         'category':categories,
#         'product':products,
#         'variants':variants,
#         "color":available_colors,
#     }
#         return render(request,'home/shop.html',context)

def product_search(request):
    query = request.GET.get('search')
    print(query,'fghjgfghfghfghfdfgfgdf')
    color_filter = request.GET.get('color')
    print(color_filter)
    sort = request.GET.get('sort')
    print(sort)

    categories = Category.objects.filter(is_activate=True)
    products = Product.objects.filter(is_activate=True)
    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()
    variants = Variation.objects.filter(is_available=True)

    if query:
        variants = Variation.filter(product__product_name__icontains=query)

    if color_filter:
        variants = variants.filter(color=color_filter)

    if sort == '1':
        variants = variants.order_by('-selling_price')
    else:
        variants = variants.order_by('selling_price')

    context = {
        'category': categories,
        'product': products,
        'variants': variants,
        'color': available_colors,
    }

    return render(request, 'home/shop.html', context)

def variant_within_category(request,category_id):


    category=Category.objects.get(id=category_id)
    print(category_id)
    categories = Category.objects.filter(is_activate=True)
    
    products = Product.objects.filter(is_activate=True)
    sub_categories = Sub_Category.objects.filter(category=category)
    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()

    try:
        # product=Product.objects.filter(category=category)
        variants =  Variation.objects.filter(product__category_id=category_id)
    except:
        variants=None
    context={
        'category':categories,
        'product':products,
        'variants':variants,
        "color":available_colors,
        'sub_categories':sub_categories,
        'category_id':category_id
    }

    return render(request,'home/shop.html',context)

def variant_within_subcategory(request,sub_category_id):


    # category=Category.objects.get(id=category_id)

    categories = Category.objects.filter(is_activate=True)
    
    products = Product.objects.filter(is_activate=True)
    
    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()

    sub_categories = Sub_Category.objects.filter(id=sub_category_id)
    try:
        # product=Product.objects.filter(category=category)
        variants =  Variation.objects.filter(product__sub_category_id=sub_category_id)
    except:
        variants=None
    context={
        'category':categories,
        'product':products,
        'variants':variants,
        "color":available_colors,
        # 'sub_categories':sub_categories.
    }

    return render(request,'home/shop.html',context)
    
def product_color_filter(request):
    
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()
    query=request.GET.get('q')
    variants=Variation.objects.filter(color=query,is_available=True)
    context={
        'category':categories,
        'product':products,
        'variants':variants,
        "color":available_colors,
    }


    return render(request,'home/shop.html',context)

def product_sort(request):
    sort=request.GET.get('sort')
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()

    if sort== '1':
        variants=Variation.objects.filter(is_available=True).order_by('-selling_price')

    else:
         variants=Variation.objects.filter(is_available=True).order_by('selling_price')

    context={
        'category':categories,
        'product':products,
        'variants':variants,
        "color":available_colors,
    }

    return render(request,'home/shop.html',context)
