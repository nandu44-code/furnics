from django.urls import path
from . import views


urlpatterns = [
    
       path('',views.admin_login,name='admin_login'),
       path('admin-home/',views.adminhome,name='admin_home'),
       path('admin-logout',views.adminlogout,name='admin_logout'),

       path('users/',views.users,name='users'),
       path('block/<int:user_id>/',views.block_user,name='block_user'),
       path('sales-report-pdf/', views.sales_report_pdf_download, name='sales_report_pdf'),

       path('categories/',views.categories,name='categories'),
       path('add-categories/',views.add_categories,name='add_categories'),
       path('edit-categories/<int:category_id>/',views.edit_categories,name='edit_categories'),
       path('delete-categories/<int:category_id>/',views.delete_categories,name='delete_categories'),

       path('sub-categories/',views.sub_categories,name='sub_categories'),
       path('add-subcategories/',views.add_subcategories,name='add_subcategories'),
       path('edit-subcategories/<int:subcategory_id>/',views.edit_subcategories,name='edit_subcategories'),
       path('delete-subcategories/<int:subcategory_id>/',views.delete_subcategories,name='delete_subcategories'),

       path('orders',views.orders,name="orders"),
       path("orders-details/<int:order_id>/",views.orders_details,name="orders_details"),
       path('order-status',views.order_status,name="order_status"),

       path('get-sales-revenue/', views.get_sales_revenue,name='get_sales_revenue'),
       # path('sales-report-selected-date',views.sales_report_selected_date,name='sales_report_selected_date'),

       path('coupon',views.coupon,name='coupon'),
       path('add-coupon',views.add_coupon,name="add_coupon"),
       path('edit-coupon/<int:coupon_id>/',views.edit_coupon,name="edit_coupon"),
       path('block-coupon/<int:coupon_id>/',views.block_coupon,name="block_coupon"),

       path('banner',views.banner,name="banner"),
       path('add-banner',views.add_banner,name="add_banner"),
       path('edit-banner/<int:banner_id>/',views.edit_banner,name="edit_banner"),
       path('remove-banner/<int:banner_id>/',views.remove_banner,name="remove_banner")
]

