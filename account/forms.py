from django import forms
from django.contrib import auth

from . import models

# from accounts.models import UserInfo, RoleList, PermissionList

DEFAULT_CLASS = {'class': 'form-control'}
VALID_CLASS = {'class': 'form-control is-valid'}
INVALID_CLASS = {'class': 'form-control is-invalid'}


class BootstrapBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 给实例对象的每一个字段添加class
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginUserForm(forms.Form):
    username = forms.CharField(label='用户名', error_messages={'required': '用户名不能为空'},
                               widget=forms.TextInput(attrs=DEFAULT_CLASS), help_text="请填写用户名")
    password = forms.CharField(label='密 码', error_messages={'required': '密码不能为空'},
                               widget=forms.PasswordInput(attrs=DEFAULT_CLASS), help_text="请填写密码")

    # v_code = forms.CharField(label="验证码", error_messages={'required': "验证码不能为空"},
    #                          widget=forms.TextInput(attrs=DEFAULT_CLASS), help_text="请填写验证码"
    #                          )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean(self):

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # print(self.fields['username'].widget.attrs["class"], self.fields['username'].widget.attrs)

        if username and password:
            print(username, password)
            self.user_cache = auth.authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                # self.fields['username'].widget.attrs.update(INVALID_CLASS)
                # self.fields['username'].help_text = "账号密码不匹配"
                # self.fields['password'].widget.attrs.update(INVALID_CLASS)
                # self.fields['password'].help_text = ""
                self.add_error('username', '账号密码不匹配')
                self.add_error('password', '账号密码不匹配')
                raise forms.ValidationError(u'账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class RegisterForm(BootstrapBaseForm):
    re_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(),
    )

    class Meta:
        model = models.UserInfo
        fields = ["email", "username", "password", "re_password"]

    # 验证邮箱
    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = models.UserInfo.objects.filter(email=email)
        if is_exist:
            self.add_error("email", "邮箱已被注册")
            return forms.ValidationError("邮箱已被注册")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            # self.add_error("password", "密码不要少于6位")
            raise forms.ValidationError("密码不要少于6位")
        return password

    # 验证用户名
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            self.add_error("username", "用户名已被注册")
            raise forms.ValidationError("用户名已被注册")
        return username

    # 验证密码
    def clean(self):
        pwd = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("re_password")
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            self.add_error("re_password", "两次密码不一致")
            raise forms.ValidationError("两次密码不一致")
