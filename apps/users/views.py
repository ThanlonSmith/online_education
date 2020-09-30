from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm, UserLoginForm
from .models import UserProfile
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, logout, login


# Create your views here.
def index(request):
    return render(request, 'index.html')


# 用户注册功能模块
def register(request):
    if request.method == "GET":
        return render(request, 'users/register.html')
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']
            user_is_exists = UserProfile.objects.filter(
                Q(username=email) | Q(email=email)).exists()  # 使用 exists比使用 count 或者直接判断 QuerySet 更加高效
            if user_is_exists:
                msg = "用户已经存在，请直接 <a style='color:green;font-weight:bold' href='/users/login'>登录</a> 吧！"
                msg = mark_safe(msg)
                return render(request, 'users/register.html', {
                    'msg': msg
                })
            else:
                user = UserProfile()
                user.username = email
                user.set_password(password)
                user.email = email
                user.save()
                return redirect('index')
        else:
            return render(request, 'users/register.html', {
                'user_register_form': user_register_form
            })


# 用户登录功能模块
def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                # return redirect('index')
                # 可以加参数
                login(request,user)
                return redirect(reverse('index'))
            return render(request, 'users/login.html', {
                'msg': '用户名或密码不正确！'
            })
        return render(request, 'users/login.html', {
            'user_login_form': user_login_form
        })
    return render(request, 'users/login.html')


# 用户退出功能模块
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))
