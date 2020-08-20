from django.db import models
from product.models import product_table, sellers_product, seller_details
from datetime import date, timedelta
from vs24.models import Registration

class cart_table(models.Model):
    user = models.ForeignKey(Registration, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product_table, on_delete=models.CASCADE)
    seller = models.ForeignKey(sellers_product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = (('product_id', 'seller', 'user'),)

    def __str__(self):
        return self.user.Email

# order_id = models.CharField(max_length=450)
class checkout_order(models.Model):
    order_id = models.CharField(max_length=30)
    user = models.ForeignKey(Registration, on_delete=models.CASCADE)
    seller = models.ForeignKey(seller_details, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product_table, on_delete=models.CASCADE)
    process = models.CharField(max_length=30, default='Failed')
    status = models.BooleanField(default=True)
    name = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=255, default="")
    land_mark = models.CharField(max_length=150, default="")
    pincode = models.CharField(max_length=20, default="")
    mobile = models.CharField(max_length=15, default="")
    current_date = models.DateField(auto_now=False, auto_now_add=False,  blank=True)
    current_time = models.TimeField(auto_now=False, auto_now_add=False,  blank=True)

    def __str__(self):
        return self.order_id
#
#
#
