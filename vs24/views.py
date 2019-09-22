from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Registration

def index(request):
    return render(request, 'vs24/index.html')


def home(request):
    return render(request, 'vs24/home.html')


def login(request):
    return render(request, 'vs24/login.html')


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
    return render(request, 'vs24/signup.html')


def product_detail_views(request):
    return render(request, 'vs24/product-detail-views.html')


def cart(request):
    return render(request, 'vs24/product_cart.html')


# testing git