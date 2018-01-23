#coding:utf-8
import random
from django.core.mail import send_mail
import string
from user.models import EmailVerifyCode,Profile

EMAIL_FROM = "w1638881893@163.com"

def send_password_email(email):
    email_record = EmailVerifyCode()
    code = ''.join(random.sample(string.ascii_letters + string.digits, 20))  # 注册获取16位长度的字符
    email_record.code = code
    email_record.email = email
    email_record.save()
    nick_name = Profile.objects.get(email=email).nickname
    email_title = "{0} - 重置密码".format(nick_name)
    email_body = "请点击下面的链接重置你的密码：http://www.example.com/setpassword?code={0}".format(code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    return send_status
