from django import forms
from captcha.fields import CaptchaField


class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=15,
        error_messages={
            'required': '必须填写密码',
            'min_length': '密码至少6位',
            'max_length': '密码不超过15位'
        })
    captcha = CaptchaField()


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=15,
        error_messages={
            'required': '必须填写密码',
            'min_length': '密码至少6位',
            'max_length': '密码不超过15位'
        })
    captcha = CaptchaField()