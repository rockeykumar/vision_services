from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect
import math
from cart.models import cart_table
from product.models import product_table, sellers_product, product_categories, seller_details, product_details
from .models import Registration


def count(request):
    try:
        total_count = 0
        if request.session.get('session') is not None:
            user_obj = Registration.objects.get(Q(Email=request.session.get('session')))
            cart_obj = cart_table.objects.filter(user=user_obj)

            for i in cart_obj:
                total_count += int(i.count)
            return total_count
        else:
            print("count 0")
            return total_count
    except:
        return HttpResponse("cart count function in vs24/view app")

def index(request):
    try:
        return render(request, 'vs24/index.html')
    except:
        return HttpResponse("yes")

def home(request):
    try:
        product = product_table.objects.all()
        product_price = sellers_product.objects.all()
        if request.session.get('session') is not None:
            match = Registration.objects.get(Q(Email=request.session.get('session')))
            return render(request, 'vs24/home.html', {
                'product': product,
                'product_price': product_price,
                'total_count': count(request),
                'sr': match
            })
        else:
            return render(request, 'vs24/home.html', {
                'product': product,
                'product_price': product_price,
                'total_count': count(request),
            })
    except:
        return render(request, 'vs24/home.html')


def login(request):
    if request.session.get('session') is not None:
        return redirect('home')

    if request.method == 'POST':
        try:
            u_name = request.POST["username"]
            pass_word = request.POST["psssword"]
            login_obj = Registration.objects.filter(Q(Email=u_name)).first()
            if login_obj is not None:
                if login_obj.Password == pass_word:
                    request.session['session'] = u_name
                    return redirect('home')
                else:
                    return render(request, 'vs24/login.html', {'total_count': count(request)})
            else:
                return render(request, 'vs24/login.html', {'total_count': count(request)})
        except:
            return HttpResponse("Exception...!")
    return render(request, 'vs24/login.html', {'total_count': count(request)})


def signup(request):
    if request.method == 'POST':
        Fname = request.POST['name'].upper()
        Lname = request.POST['lname'].upper()
        Email = request.POST['e_mail']
        Mobile = request.POST['mobile']
        Password = request.POST['password']
        Cpassword = request.POST['Conf-password']

        if Password != Cpassword:
            notification = {'note': 'Password did not match...!',
                            'FName': Fname,
                            'LName': Lname,
                            'Email': Email,
                            'Mobile': Mobile
                            }
            return render(request, 'vs24/signup.html', notification)

        obj = Registration.objects.filter(Q(Email=Email)).first()
        if obj is not None:
            notification = {'note': "Already Exits...!",
                            'FName': Fname,
                            'LName': Lname,
                            'Mobile': Mobile
                            }
            return render(request, 'vs24/signup.html', notification)

        reg = Registration(
            FName=Fname,
            LName=Lname,
            Email=Email,
            Mobile=Mobile,
            Password=Password
        )
        reg.save()
        return redirect('login')
    return render(request, 'vs24/signup.html', {'total_count': count(request)})


def slug_msg(request, id):
    print(id)
    return render(request, 'vs24/product-detail-views.html')



def cart(request):
    return render(request, 'vs24/product_cart.html')


# testing git
def logout_view(request):
    logout(request)
    return redirect('home')


def font_test(request):
    return render(request, 'vs24/font_testing.html')


# 26/03/2020 add product data to database
def insert_product_database(request):
    categories = product_categories.objects.all()
    seller_name = seller_details.objects.all()
    pid = product_table.objects.all().count()  # total no.s add in product table
    pid = pid + 1
    if request.method == "POST":
        p_id = request.POST["product_id"]
        p_category = request.POST["product_categories"]
        p_model = request.POST["product_model"]
        p_title = request.POST["product_title"]
        p_brand = request.POST["product_brand"]

        cat = product_categories.objects.filter(Q(product_category=p_category)).first()
        pro = product_table(
            product_id=p_id,
            product_category=cat,
            product_model=p_model,
            product_title=p_title,
            product_brand=p_brand
        )
        pro.save()
        return render(request, 'product/add_product_seller.html', {"p_id": p_id, 'seller_name': seller_name})
    else:
        return render(request, 'product/insert_product.html', {'categories': categories, 'pid': pid})


def add_product_seller(request):
    mod_id = request.POST["model_id"]
    s_name = request.POST["seller_name"]
    pro_price = request.POST["price"]
    dis = int(request.POST["discount"])

    net_price = ((int(pro_price) * (100 - int(dis)))/100)
    print(net_price)
    net_price = str(math.ceil(net_price))
    print(net_price)

    seller_id_obj = product_table.objects.filter(Q(product_id=mod_id)).first()
    seller_name_obj = seller_details.objects.filter(Q(seller_name=s_name)).first()

    obj_seller = sellers_product(
        product_model=seller_id_obj,
        seller_name=seller_name_obj,
        product_price=pro_price,
        product_discount=dis,
        product_discount_price=net_price
    )
    obj_seller.save()
    return render(request, 'product/product_detail.html', {"p_id": mod_id})


def add_product_detail(request):
    if request.method == "POST":
        pro_det_id = request.POST.get("product_detail_id", "")
        img1 = request.FILES.get("doc_upload_1", "")
        img2 = request.FILES.get("doc_upload_2", "")
        img3 = request.FILES.get("doc_upload_3", "")
        img4 = request.FILES.get("doc_upload_4", "")
        img5 = request.FILES.get("doc_upload_5", "")
        img6 = request.FILES.get("doc_upload_6", "")
        img7 = request.FILES.get("doc_upload_7", "")
        pro_desc = request.POST.get("description", "")
        #
        product_detail_id_obj = product_table.objects.filter(Q(product_id=pro_det_id)).first()
        pro_detail_obj = product_details(
            product_model=product_detail_id_obj,
            product_image1=img1,
            product_image2=img2,
            product_image3=img3,
            product_image4=img4,
            product_image5=img5,
            product_image6=img6,
            product_image7=img7,
            product_description=pro_desc
        )
        pro_detail_obj.save()
        return HttpResponse("Product Add Successfully.........!")
    return render(request, 'product/product_detail.html')


