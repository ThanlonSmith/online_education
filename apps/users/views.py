from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import UserRegisterForm, UserLoginForm, UserForgetPwdForm, UserResetForm
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
                'msg': '用户名或密码不正确！',
                'user_login_form': user_login_form
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


# 向用户发送用于重置密码的邮箱验证码
def user_forget_pwd(request):
    if request.method == 'GET':
        user_forget_pwd_form = UserForgetPwdForm()
        return render(request, 'users/forget-pwd.html', {
            'user_forget_pwd_form': user_forget_pwd_form
        })
    else:
        user_forget_pwd_form = UserForgetPwdForm(request.POST)
        if user_forget_pwd_form.is_valid():
            email = user_forget_pwd_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(email=email)
            if user_list.exists():
                send_email_code(email, 2)
                return HttpResponse('请尽快去您的邮箱重置密码！')
            else:
                return render(request, 'users/forget-pwd.html', {
                    'msg': '用户不存在！'
                })
        else:
            return render(request, 'users/forget-pwd.html', {
                'user_forget_pwd_form': user_forget_pwd_form
            })


def user_reset(request, code):
    if code:
        if request.method == 'GET':
            return render(request, 'users/password-reset.html', {
                'code': code
            })
        else:
            user_reset_form = UserResetForm(request.POST)
            if user_reset_form.is_valid():
                password = user_reset_form.cleaned_data['password']
                password2 = user_reset_form.cleaned_data['password2']
                if password == password2:
                    code_obj_list = EmailVerifyCode.objects.filter(
                        code=code)  # <QuerySet [<EmailVerifyCode: VmUIe9CS>]>
                    if code_obj_list.exists():
                        email = code_obj_list.first().email
                        user_obj_list = UserProfile.objects.filter(email=email)
                        if user_obj_list.exists():
                            current_user = user_obj_list.first()
                            print(current_user)
                            current_user.set_password(password)
                            current_user.save()
                            return redirect(reverse('users:login'))
                        else:
                            pass
                    else:
                        pass
                else:
                    return render(request, 'users/password-reset.html', {
                        'msg': '两次密码不一致！',
                        'code': code
                    })
            else:
                return render(request, 'users/password-reset.html', {
                    'user_reset_form': user_reset_form,
                    'code': code
                })
    pass
