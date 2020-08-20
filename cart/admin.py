from django.contrib import admin

from cart.models import cart_table, checkout_order

class cart_table_admin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['user', 'seller', 'product_id', 'count']

admin.site.register(cart_table, cart_table_admin)
admin.site.register(checkout_order)
