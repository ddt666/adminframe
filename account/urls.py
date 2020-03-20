from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login', views.login, name="login"),

    path('get_valid_img', views.get_valid_img, name="get_valid_img"),

    path('register', views.register, name="register"),
]
