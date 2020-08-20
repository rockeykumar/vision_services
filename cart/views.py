import datetime, time
import math
from product.views import index
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from vs24.views import count
from cart.forms import card_form
from cart.models import cart_table, checkout_order
from product.models import sellers_product, product_details, product_table, seller_details
from vs24.models import Registration
from django.views.decorators.csrf import csrf_exempt
from cart.Paytm import Checksum


#'MID': 'WorldP64425807474247'
#MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
MERCHANT_KEY = 'fsCXTDIoIkJ_@&d6'


def cart(request):
    print("********************************cart app click add to cart button**************************")
    try:
        if request.method == 'POST':
            if request.session.get('session') is not None:
                form = card_form(request.POST)
                if form.is_valid():

                    p_id = form.cleaned_data.get("pro_id")
                    print(p_id)
                    pro_obj = product_table.objects.get(product_id=p_id)

                    # p_seller = request.POST.get('add_to_cart_seller')
                    p_seller = form.cleaned_data.get("pro_seller")
                    seller = seller_details.objects.get(seller_name=p_seller)
                    seller_obj = sellers_product.objects.get(Q(seller_name=seller) and Q(product_model=pro_obj))
                    print(1)
                    user_obj = Registration.objects.filter(Q(Email=request.session.get('session'))).first()
                    print(user_obj)
                    cart_obj = cart_table.objects.filter(Q(user=user_obj))
                    print(cart_obj)
                    if request.method == 'POST':
                        for i in cart_obj:
                            print("if")
                            if i.product_id == pro_obj and i.count < 3:
                                print(i.product_id.product_id)
                                i.count += 1
                                i.save()
                                print("break")
                                break
                            elif i.product_id == pro_obj and i.count == 3:
                                return redirect('cart_list_views')
                        else:
                            obj = cart_table(
                                user=user_obj,
                                product_id=pro_obj,
                                seller=seller_obj,
                                count=1
                            )
                            obj.save()
                    return redirect('cart_list_views')
                print("Exception occur")
                return redirect('cart_list_views')
            else:
               return redirect('login')
        else:
            return redirect('cart_list_views')
        return redirect('cart_list_views')
    except:
        return HttpResponse("*** Exception *****cart app click add to cart button****************")


def cart_list_views(request):
    try:
        if request.session.get('session') is not None:
            user_obj = Registration.objects.get(Q(Email=request.session.get('session')))
            cart_obj = cart_table.objects.filter(user=user_obj)
            desc_obj = product_details.objects.all
            dic_price = 0
            real_price = 0
            total_count = 0

            for i in cart_obj:
                dic_price += (int(i.seller.product_discount_price)) * (int(i.count))
                real_price += (int(i.seller.product_price)) * (int(i.count))
                total_count += int(i.count)

            saving = real_price - dic_price
            # saving = math.ceil(saving*100)/100
            print(saving)
            context = {
                'desc_obj': desc_obj,
                'cart_obj': cart_obj,
                'total_count': total_count,
                'dic_price': dic_price,
                'saving': saving,
                'Date': datetime.date.today() + datetime.timedelta(days=8),
                'sr': user_obj
            }
            print("****************** add button on. of item add repeat session successfully")
            return render(request, 'cart/product_cart.html', context)
        else:
            context = {'total_count': count(request)}
            return render(request, 'cart/product_cart.html', context)
    except:
        return HttpResponse("cart list exception")

def ajax_dynamical(request):
    try:
        if request.session.get('session') is not None:
            user_obj = Registration.objects.get(Q(Email=request.session.get('session')))
            id = request.GET.get('id')
            seller = request.GET.get('seller')
            nature = request.GET.get('nature')

            pro_obj = product_table.objects.get(product_id=id)
            seller = seller_details.objects.get(seller_name=seller)

            seller_obj = sellers_product.objects.get(Q(seller_name=seller) and Q(product_model=pro_obj))

            cart_obj = cart_table.objects.filter(user=user_obj)

            count_incr = 0
            for i in cart_obj:
                if i.product_id == pro_obj:
                    if nature == 'add' and i.count < 3:
                        i.count += 1
                    elif nature == 'minus' and i.count > 1:
                        i.count -= 1
                    i.save()
                    count_incr = i.count
                    break

            dic_price = 0
            real_price = 0
            total_count = 0

            for i in cart_obj:
                dic_price += (int(i.seller.product_discount_price)) * (int(i.count))
                real_price += (int(i.seller.product_price)) * (int(i.count))
                total_count += int(i.count)

            saving = real_price - dic_price

            user = {
                'total_count': total_count,
                'dic_price': dic_price,
                'saving': saving,
                'count_incr': count_incr
            }

            data = {
                'user': user
            }
            return JsonResponse(data)
    except:
        return HttpResponse("******* cart view app ajax dynamically function**************")

def delete_item(request):
    remove_id = request.GET.get('remove_id')
    cart_item_delete = get_object_or_404(cart_table, pk=remove_id)
    cart_item_delete.delete()
    print(cart_item_delete)


    user_obj = Registration.objects.get(Email='golu@gmail.com')
    cart_obj = cart_table.objects.filter(user=user_obj)

    dic_price = 0
    real_price = 0
    total_count = 0

    for i in cart_obj:
        dic_price += (int(i.seller.product_discount_price)) * (int(i.count))
        real_price += (int(i.seller.product_price)) * (int(i.count))
        total_count += int(i.count)
    else:
        print('empty')

    saving = real_price - dic_price

    user = {
        'total_count': total_count,
        'dic_price': dic_price,
        'saving': saving,
        'remove_id': remove_id
    }


    data = {
        'user': user
    }
    return JsonResponse(data)

def order_Place(request):
    if request.method == "POST":
        if request.session.get('session') is not None:
            user_obj = Registration.objects.get(Q(Email=request.session.get('session')))
            net_amt = request.POST["amount"]
            return render(request, 'cart/orderPlaceAddress.html', {'sr': user_obj, 'total_count': count(request), 'total_price': net_amt})
        return redirect('login')
    return redirect('login')


# def order_count(request):
#     total_count = "00000000"
#     try:
#         odr_count = checkout_order.objects.all()
#         total_count = len(odr_count) + 1
#         total_count = str(total_count)
#         while len(total_count) < 7:
#             total_count = "0"+total_count
#         return total_count
#     except:
#         return total_count


def order_count(request):
    date_time_id = str(datetime.datetime.now())
    order_id = ''
    for s in date_time_id:
        if (s.isnumeric()) == True: 
            order_id = order_id + s

    return order_id


def confirmOrder(request):
    if request.method == "POST":
        if request.session.get('session') is not None:
            user_obj = Registration.objects.get(Q(Email=request.session.get('session')))
            usr_eml = user_obj.Email
            cart_obj = cart_table.objects.filter(Q(user=request.session.get('session')))
            c_name = request.POST["customer_full_name"]
            c_address = request.POST["customer_address"]
            c_land_mark = request.POST["customer_land_mark"]
            c_pincode = request.POST["customer_pincode"]
            c_mobile = request.POST["customer_mobile"]
            net_amt = request.POST["cnfrm_price"]
            current_date = datetime.date.today()
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            or_id = order_count(request)

            print(current_date)
            print((datetime.datetime.now()))
            for c in cart_obj:
                seller = seller_details.objects.get(Q(seller_name=c.seller))
                for i in range(c.count):
                    order_obj = checkout_order(
                        user=user_obj,
                        seller=seller,
                        order_id=or_id,
                        product_id=c.product_id,
                        name=c_name,
                        address=c_address,
                        land_mark=c_land_mark,
                        pincode=c_pincode,
                        mobile=c_mobile,
                        current_date=current_date,
                        current_time=current_time
                    )
                    order_obj.save()

            # 'ORDER_ID': or_id,
            param_dict = {
                'MID': 'DlPVbc40643401016043',
                'ORDER_ID': or_id,
                'TXN_AMOUNT': str(net_amt),
                'CUST_ID': usr_eml,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/cart/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'cart/paytm.html', {'param_dict': param_dict})
    return redirect('login')

#
@csrf_exempt
def handlerequest(request):          #paytm will send post request here
    try:
        form = request.POST
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]

        verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
        chckout_obj = checkout_order.objects.filter(Q(order_id=response_dict['ORDERID'])).first()
        user_obj = Registration.objects.get(Q(Email=chckout_obj.user))

        if verify:
            print(response_dict['RESPCODE'])
            if response_dict['RESPCODE'] == '01':
                print("successfully...!")
                chk_obj = checkout_order.objects.filter(Q(order_id=response_dict['ORDERID']))
                for i in chk_obj:
                    update_obj = checkout_order.objects.get(Q(pk=i.pk))
                    update_obj.process = "Pending"
                    update_obj.save()
            else:
                chk_obj = checkout_order.objects.filter(Q(order_id=response_dict['ORDERID']))
                for i in chk_obj:
                    update_obj = checkout_order.objects.get(Q(pk=i.pk))
                    update_obj.process = "Failed"
                    update_obj.save()
                print("Sorry your order not successfully placed because "+response_dict['RESPMSG'])

        print("pass 5")
        cart_table.objects.filter(Q(user=user_obj)).delete()
        return render(request, 'cart/paymentStatus.html', {'response': response_dict, 'sr': user_obj, 'total_count': count(request)})
    except:
        return HttpResponse("handlerequest cart app")






#
#
# @csrf_exempt
# def handlerequest(request):          #paytm will send post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]
#
#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     print("------------------------------------------------------------------")
#     print(verify)
#     print("------------------------------------------------------------------")
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print("successfully...!")
#         else:
#             print("Sorry your order not successfully placed because "+response_dict['RESPMSG'])
#
#     return render(request, 'cart/paymentStatus.html', {'response': response_dict})
