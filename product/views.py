from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from cart.forms import card_form
from product.models import product_table, sellers_product, product_details, product_categories
from vs24.models import Registration
from vs24.views import count


def index(request, name=None, slug=None):
    try:
        print('*******************************product app view index function*********************** ')
        obj = product_table.objects.get(product_slug=slug)
        product_price = sellers_product.objects.filter(product_model=obj)
        product_desc = product_details.objects.get(product_model=obj)
        price_list = []
        for i in product_price:
            price_list.append(i.product_discount_price)

        minp = min(price_list)
        min_price_obj = sellers_product.objects.filter(product_discount_price=minp).first()

        desc = product_desc.product_description.split("\n")
        if request.session.get('session') is not None:
            match = Registration.objects.get(Q(Email=request.session.get('session')))
            return render(request, 'vs24/product-detail-views.html', {
                'obj': obj,
                'product_price': product_price,
                'min_price_obj': min_price_obj,
                'desc': desc,
                'total_count': count(request),
                'sr': match
            })
        else:
            return render(request, 'vs24/product-detail-views.html', {
                'obj': obj,
                'product_price': product_price,
                'min_price_obj': min_price_obj,
                'desc': desc,
                'total_count': count(request)
            })
    except:
        return HttpResponse("product view index function")


def dynamic_categories(request):
    try:
        print("*******************************product view in dynamin categories function*****************************")
        category = request.GET.get('Category')
        cat = product_categories.objects.get(product_category=category)
        obj = product_table.objects.filter(product_category=cat)
        if request.session.get('session') is not None:
            match = Registration.objects.get(Q(Email=request.session.get('session')))
            param = {'obj': obj, 'category': category, 'total_count': count(request), 'sr': match}
            return render(request, 'product/list_product_views.html', param)
        else:
            param = {'obj': obj, 'category': category, 'total_count': count(request)}
            return render(request, 'product/list_product_views.html', param)
    except:
        return HttpResponse("Not worked till now coming soon....!")

