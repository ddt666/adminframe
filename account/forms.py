from django import forms
from django.contrib import auth

# from accounts.models import UserInfo, RoleList, PermissionList

DEFAULT_CLASS = {'class': 'form-control'}
VALID_CLASS = {'class': 'form-control is-valid'}
INVALID_CLASS = {'class': 'form-control is-invalid'}


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
            self.user_cache = auth.authenticate(username=username, password=password)
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
