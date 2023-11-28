
from django.urls import path
from . import views
from .views import product_color_filter


urlpatterns = [
    
      path('',views.homepage,name="homepage"),
      path('view-shop',views.view_shop,name="shop_page"),
      path('view-subcategory/<int:category_id>/',views.view_subcategory,name="sub_category_page"),
      path('display-products/<int:sub_category_id>/',views.display_products,name="display_product"),
      
      path('product-details/<int:variant_id>/',views.product_details,name="product_details"),
      path('variant_select/<int:variant_id>/',views.variant_select,name="variant_select"),

      path('variant-within-subcategory/<int:sub_category_id>/',views.variant_within_subcategory,name='variant_within_subcategory'),
      path('variant-within-category/<int:category_id>/',views.variant_within_category,name='variant_within_category'),

      path('product-search',views.product_search,name="product_search"),
      path('filter-color',views.product_color_filter,name="product_color_filter"),
      path('product-sort',views.product_sort,name="product_sort")
      

]