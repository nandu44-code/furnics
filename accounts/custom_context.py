# from carts.models import Cart, CartItem


# def cartitemcount(request):
#     count=0
#     if request.user:
#         user=request.user
#         cart=Cart.objects.get(user=user)
#         cartitem=CartItem.objects.filter(cart=cart)
        
#         for i in cartitem:
#             count+=1
        
#     return {
#         'cartitemcount':count
#     }