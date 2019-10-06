from django.contrib import admin
from .models import product_categories, product_table, product_details, seller_details, sellers_product

admin.site.register(product_categories)
admin.site.register(product_table)
admin.site.register(product_details)
admin.site.register(seller_details)
admin.site.register(sellers_product)
