from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import UserRegisterForm, UserLoginForm
from .models import UserProfile, EmailVerifyCode
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, logout, login
from tools.send_email_tool import send_email_code


# Create your views here.
def index(request):
    return render(request, 'index.html')


# 用户注册功能模块
def user_register(request):
    if request.method == "GET":
        # 这里使用UserRegisterForm不是为了验证，而是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'users/register.html', {
            'user_register_form': user_register_form
        })
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
                # user.image =
                user.save()
                send_email_code(email, 1)
                return HttpResponse('请尽快前往您的邮箱激活，否则无法登录！')
                # return redirect('index')
        else:
            return render(request, 'users/register.html', {
                'user_register_form': user_register_form
            })


# 用户登录功能模块
def user_login(request):
    if request.method == 'GET':
        user_login_form = UserLoginForm()
        return render(request, 'users/login.html', {
            'user_login_form': user_login_form
        })
    else:
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                if user.is_start:
                    # return redirect('index')
                    # 可以加参数
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return HttpResponse('请到邮箱中激活用户，否则无法登录系统！')
            return render(request, 'users/login.html', {
                'msg': '用户名或密码不正确！'
            })
        return render(request, 'users/login.html', {
            'user_login_form': user_login_form
        })


# 用户退出功能模块
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


# 用户激活(这里还遗留一个问题：如果产生的随机码有重复，一个验证码对不同的邮箱，可能会出问题)
def user_activate(request, code):
    if code:
        code_obj_list = EmailVerifyCode.objects.filter(code=code)  # <QuerySet [<EmailVerifyCode: ZW417PgB>]>
        if code_obj_list.exists():
            code_obj = code_obj_list.first()  # verify_code_obj = code_obj_list[0]
            email = code_obj.email
            user_list = UserProfile.objects.filter(username=email)
            if user_list.exists():
                user = user_list.first()
                user.is_start = True
                user.save()
                return redirect(reverse('users:login'))