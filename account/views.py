from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib import auth

from .forms import LoginUserForm
from account.utils.auth import get_valid
from utils.response import BaseResponse
from .utils.auth import send_email_code
from .utils.common import get_random_int


# Create your views here.
def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        res = BaseResponse()

        v_code = request.POST.get("v_code", "").lower()
        if v_code == request.session["v_code"]:
            # username = request.POST.get("username")
            # password = request.POST.get("password")
            #
            # user_obj = rbac.authenticate(username=username, password=password)
            # if user_obj:
            #     rbac.login(request,user_obj)

            form = LoginUserForm(request, data=request.POST)
            if form.is_valid():
                auth.login(request, form.get_user())

                res.msg = "登录成功"
                return JsonResponse(res.dict)
            else:
                res.code = -1

                res.msg = form.errors

        else:
            res.code = -1
            res.msg = {"v_code": ["验证码出错"]}
        return JsonResponse(res.dict)

    else:
        form = LoginUserForm(request)
    return render(request, "login.html", {"form": form})


def get_valid_img(request):
    img_data, v_code = get_valid(length=5, width=135, height=40)
    request.session['v_code'] = v_code
    print("v_code", v_code)
    return HttpResponse(img_data, content_type="image/png")


def register(request):
    res = BaseResponse()

    if request.method == "POST":
        to_email = request.POST.get("email")
        if to_email:
            email_code = get_random_int()
            ret = send_email_code(email_code, [to_email])
            if ret == 1:
                request.session['email_code'] = email_code
                pass
            else:
                pass

        return JsonResponse(res.dict)
    else:
        pass

    return render(request, "register.html")
