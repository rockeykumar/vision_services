from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from vision.utils import unique_slug_generator

class product_categories(models.Model):
    product_category = models.CharField(max_length=100)

    def __str__(self):
        return self.product_category


class product_table(models.Model):
    product_category = models.ForeignKey(product_categories, on_delete=models.CASCADE)
    product_model = models.CharField(max_length=30, primary_key=True)
    product_slug = models.SlugField(max_length=450, blank=True, null=True)
    product_title = models.CharField(max_length=150)
    product_brand = models.CharField(max_length=150)
    product_add_date = models.DateTimeField(default=timezone.now)


class product_details(models.Model):
    product_model = models.ForeignKey(product_table, on_delete=models.CASCADE)
    product_image1 = models.FileField(upload_to='product/gallery/')
    product_image2 = models.FileField(upload_to='product/gallery/')
    product_image3 = models.FileField(upload_to='product/gallery/')
    product_image4 = models.FileField(upload_to='product/gallery/')
    product_image5 = models.FileField(upload_to='product/gallery/')
    product_image6 = models.FileField(upload_to='product/gallery/')
    product_image7 = models.FileField(upload_to='product/gallery/')
    product_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product_model.product_title


class seller_details(models.Model):
    seller_name = models.CharField(max_length=30, primary_key=True )
    FName = models.CharField(max_length=30)
    LName = models.CharField(max_length=30)
    Email = models.EmailField(max_length=30)
    Mobile = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)

    def __str__(self):
        return self.seller_name


class sellers_product(models.Model):
    product_model = models.ForeignKey(product_table, on_delete=models.CASCADE)
    seller_name = models.ForeignKey(seller_details, on_delete=models.CASCADE, primary_key=True)
    product_price = models.CharField(max_length=10)
    product_discount = models.CharField(max_length=3, default="", blank=True)

    def __str__(self):
        return self.product_model.product_model



def slug_generator(sender, instance, *args, **kwargs):
    if not instance.product_slug:
        instance.product_slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=product_table)