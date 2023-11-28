from django.contrib import admin
from . models import Coupon, Product, VariantImage, Variation
# Register your models here.
admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(VariantImage)
admin.site.register(Coupon)
