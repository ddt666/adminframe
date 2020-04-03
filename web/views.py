from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return render(request, "index.html")


def customer_list(request):
    print("c"*120)
    return render(request, "customer_list.html")


def customer_add(request):
    return render(request, "customer_add.html")


def payment_list(request):
    return render(request, "payment_list.html")


def payment_add(request):
    return render(request, "payment_add.html")


def my_customer_list(request):
    print("hhhhhhhhhhhhhhhhhh"*10)
    return render(request, "my_customer_list.html")

def single_menu(request):
    return render(request ,'')
