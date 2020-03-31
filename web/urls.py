from django.urls import path, re_path

from . import views

app_name = 'web'
urlpatterns = [
    re_path('^$', views.index, name='index'),
    re_path('^customer/list', views.customer_list, name='customer_list'),
    re_path('^my_customer/list', views.my_customer_list, name='my_customer_list'),
    re_path('customer/add', views.customer_add, name='customer_add'),
    re_path('payment/list', views.payment_list, name='payment_list'),
    re_path('payment/add', views.payment_add, name='payment_add'),

]
