from django.contrib import admin
from .models import product_categories, product_table, product_details, seller_details, sellers_product


class product_table_admin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['product_category', 'product_model', 'product_title', 'product_brand', 'product_add_date']

admin.site.register(product_table, product_table_admin)


admin.site.register(product_categories)
admin.site.register(product_details)
admin.site.register(seller_details)


class seller_product_admin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['seller_name', 'product_model']

admin.site.register(sellers_product, seller_product_admin)
