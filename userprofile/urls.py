   
from django.urls import path
from . import views



urlpatterns = [
    
    path('',views.user_profile,name="user_profile"),
    path('edit-profile/<int:user_id>/',views.edit_user_profile,name="edit_user_profile"),

    path('address-view',views.address_view,name='view_address'),
    path('user-address/<int:user_id>/',views.add_address,name="add_address"),
    path('user-edit-address/<int:address_id>/',views.edit_address,name="edit_address"),
    path('user-delete-address<int:address_id>',views.delete_address,name="delete_address"),
    path('default-address',views.default_address,name="default_address"),

    path("user-orders",views.my_orders,name="my_orders"),
    path("order-details/<int:order_id>",views.order_details,name="order_details"),
    path("order-cancellation/<int:order_id>/",views.order_cancellation,name="order_cancellation"),

    path('pdf-download/<int:id>/', views.pdf_download, name='pdf_download'),
    
    path('order-return/<int:order_id>/',views.order_return,name="order_return"),

    path('user-wallet',views.user_wallet,name="user_wallet")

]   









