import uuid

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import LoginUserForm, RegisterForm, IForgotForm, ResetPasswordForm
from account.utils.auth import get_valid
from utils.response import BaseResponse
from .utils.auth import send_email_code, send_reset_password_url
from .utils.common import get_random_int
from . import models
from rbac.service import permission


# Create your views here.
@login_required
def index(request):
    print(request.session.items())
    print("request.user", request.user)
    return render(request, "index.html")


def login(request):
    # print("request.user", request.user)
    #
    # # 当session在有效期内，进入登录页面直接跳转到index页面
    # if request.user.is_authenticated:
    #     return redirect(reverse('index'))
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

            is_remember = request.POST.get('remember') == "True"

            print("is_remember", is_remember)
            form = LoginUserForm(request, data=request.POST)
            if form.is_valid():
                auth.login(request, form.get_user())

                if is_remember:
                    # session设置7天有效期
                    request.session.set_expiry(7 * 24 * 60 * 60)
                else:
                    # 否则浏览器关闭session就失效
                    request.session.set_expiry(0)
                print("request.user", request.user)

                res.msg = "登录成功"

                # 用户权限初始化
                permission.init(request.user, request)

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
        email_code = request.POST.get("email_code")

        # 验证邮箱与验证码是否匹配
        if request.session["email_code"].get(to_email) != email_code:
            res.code = -1
            res.msg = "邮箱与验证码不匹配"
            return JsonResponse(res.dict, json_dumps_params={'ensure_ascii': False})

        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print("密码", user.password)
            user.set_password(user.password)
            form.save()
            res.msg = "用户创建成功"
        else:
            res.code = -1
            # k,v=form.errors.items()[0]

            # print(type(form.errors.values()))
            first_error = ""
            for error in form.errors.values():
                first_error = error[0]
                break

            res.msg = first_error
        return JsonResponse(res.dict, json_dumps_params={'ensure_ascii': False})
    else:
        return render(request, "register.html")


# 邮箱验证码
def email_valid(request):
    res = BaseResponse()

    if request.method == "POST":
        to_email = request.POST.get("email")
        if to_email:

            is_exist = models.UserInfo.objects.filter(email=to_email)
            if is_exist:
                res.code = -1
                res.msg = "邮箱已经注册了"
                return JsonResponse(res.dict)

            email_code = get_random_int(6)
            ret = send_email_code(email_code, [to_email])

            if ret == 1:
                request.session['email_code'] = {to_email: email_code}
                res.msg = "邮箱验证码发送成功"
            else:
                res.code = -1
                res.msg = "邮箱验证码发送失败"
        else:
            res.code = -1
            res.msg = "请填写正确邮箱"
        return JsonResponse(res.dict)


def iforgot(request):
    if request.method == "POST":
        email = request.POST.get("email")
        form = IForgotForm(data=request.POST)
        is_send_success = False
        if form.is_valid():
            reset_code = ''.join(str(uuid.uuid4()).split("-"))
            print("reset_valid", reset_code)
            ret_code = send_reset_password_url(reset_code, email)
            if ret_code == 1:
                is_send_success = True
                models.ResetPasswordCode.objects.create(code=reset_code, user=form.user_cached)
                # request.session["reset_valid"] = {reset_code: form.user_cached.id}
        else:
            print(form.errors)
    else:
        form = IForgotForm()
    return render(request, 'iforgot.html', locals())


def reset_password(request, reset_code):
    res = BaseResponse()
    res.code = 0
    if request.method == "POST":

        reset = models.ResetPasswordCode.objects.filter(code=reset_code).first()
        if reset:
            user = reset.user
            form = ResetPasswordForm(data=request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data.get("password"))
                user.save()

                reset.delete()

                res.code = 1000
                res.msg = "密码重置成功"
            else:
                res.code = -1
                res.msg = "重置失败!"
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', locals())
