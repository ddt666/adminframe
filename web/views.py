from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, "index.html")


def customer_list(request):
    return render(request, "customer_list.html")


def customer_add(request):
    return render(request, "customer_add.html")


def payment_list(request):
    return render(request, "payment_list.html")


def payment_add(request):
    return render(request, "payment_add.html")
