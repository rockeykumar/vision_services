from django.contrib import admin
from .models import product_categories, product_table, product_details, seller_details, sellers_product


class product_table_admin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['product_category', 'product_model', 'product_title', 'product_brand']

admin.site.register(product_categories)
admin.site.register(product_table, product_table_admin)
admin.site.register(product_details)
admin.site.register(seller_details)
admin.site.register(sellers_product)
