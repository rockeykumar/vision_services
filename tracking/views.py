import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from product.views import index
from cart.models import checkout_order
from product.models import product_details, product_table
from vs24.models import Registration
from vs24.views import count


def __tracking__(request):
    try:
        if request.session.get('session') is not None:
            user_obj = Registration.objects.get(Q(Email=request.session.get('session')))
            checkout_obj = checkout_order.objects.filter(user=user_obj)
            desc_obj = product_details.objects.all()
            #
            context = {
                'checkout_obj': checkout_obj,
                'desc_obj': desc_obj,
                'total_count': count(request),
                'sr': user_obj
            }
            print("****************** add button on. of item add repeat session successfully")
            return render(request, 'tracking/trackingIndex.html', context)
        else:
            context = {'total_count': count(request)}
            return render(request, 'tracking/trackingIndex.html', context)
    except:
        return HttpResponse("tracking app view exception")

def __orderStatus__(request, id=None):
    print(id)
    try:
        if request.session.get('session') is not None:
            user_obj = Registration.objects.get(Q(Email=request.session.get('session')))
            statusob = checkout_order.objects.get(Q(id=id))
            obj = product_table.objects.get(product_id=statusob.product_id)

            delivered_Date = datetime.datetime.strptime(str(statusob.current_date), '%Y-%m-%d')
            delivered_Date = delivered_Date + datetime.timedelta(days=8)
            context = {
                'obj': obj,
                'statusob': statusob,
                'total_count': count(request),
                'delivered_Date': delivered_Date,
                'sr': user_obj
            }
            print("****************** tracking apps *****************************")
            return render(request, 'tracking/__orderStatus__.html', context)
        else:
            context = {'total_count': count(request)}
            # return render(request, 'tracking/__orderStatus__.html', context)
            return redirect('login')
    except:
        return HttpResponse("tracking app view exception")


def __orderCancel__(request):
    try:
        if request.session.get('session') is not None:
            id = request.POST.get('ordercancel', '')
            cancel_obj = checkout_order.objects.get(Q(id=id))
            cancel_obj.process = 'Canceled'
            cancel_obj.save()
            return redirect('tracking')
        else:
            return redirect('login')
    except:
        return redirect('login')