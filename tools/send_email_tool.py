from apps.users.models import EmailVerifyCode
from random import randrange
from django.core.mail import send_mail
from online_education.settings import EMAIL_FROM


def get_random_code(code_length):
    code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(code_length):
        # 随机选择一个字符
        str = code_source[randrange(0, len(code_source))]
        code += str
        # code += choice(code_source)
    return code


def send_email_code(email, send_type):
    # 第一步：创建邮箱验证码对象，保存数据库，用来以后做对比
    code = get_random_code(8)
    eamil_verify_code = EmailVerifyCode()
    eamil_verify_code.email = email
    eamil_verify_code.send_type = send_type
    eamil_verify_code.code = code
    eamil_verify_code.save()

    # 第二步：正式的发邮件功能
    send_title = ''
    send_body = ''
    if send_type == 1:
        send_title = '欢迎注册D5在线教育网'
        send_body = '请点击以下链接进行激活您的账号：\n http://127.0.0.1:8001/users/activate/' + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])

    if send_type == 2:
        send_title = 'D5在线教育网重置密码'
        send_body = '请点击以下链接进行重置您的密码：\n http://127.0.0.1:8001/users/reset/' + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])

    if send_type == 3:
        send_title = 'D5在线教育网修改邮箱验证码'
        send_body = '您的验证码是：' + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])
