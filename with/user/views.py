# coding:utf-8

import datetime
import json
import os
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend  #
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import View
from .forms import *
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from utils.mixin import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from page.models import *
from utils.email_send import send_password_email

__all__ = [
    'RegisterView',
    'LoginView',
    'LogoutView',
    'CenterView',
    'UserLike',
    'MessageView',
    'SettingView',
    'PasswordView',
    'FindPasswordView',
    'SetPasswordView',

]


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        nickname = request.POST.get('nickname', '')
        email = request.POST.get('email', '')
        try:
            Profile.objects.get(email=email)  # 如果邮箱已经存在
            messages.error(request, '邮箱已存在！')
            return render(request, 'register.html')
        except ObjectDoesNotExist:
            password = request.POST.get('password', '')
            retype_password = request.POST.get('re_password', '')
            if password == retype_password:
                Profile.objects.create(username=email, nickname=nickname, email=email,
                                       password=make_password(password))
                return HttpResponseRedirect(reverse('user:login'))
            else:
                messages.error(request, '两次密码不一致，请重新输入！')
                return render(request, 'register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('page:index'))
            else:  # 用户未激活
                messages.error(request, '用户尚未激活！')
                return render(request, 'login.html')
        else:  # 用户名和密码错误
            messages.error(request, '用户名或密码错误！')
            return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('page:index'))


class CenterView(View):
    def get(self, request, uid):
        articles = Article.objects.filter(user_id=uid)
        paginator = Paginator(articles, 5)
        page = request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        topics = Topic.objects.filter(user_id=uid)
        paginator = Paginator(topics, 5)
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)

        chats = Chat.objects.filter(user_id=uid)
        paginator = Paginator(chats, 5)
        try:
            chats = paginator.page(page)
        except PageNotAnInteger:
            chats = paginator.page(1)
        except EmptyPage:
            chats = paginator.page(paginator.num_pages)

        images = Image.objects.filter(user_id=uid)
        paginator = Paginator(images, 5)
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
        return render(request, 'center.html',
                      {'articles': articles, 'topics': topics, 'chats': chats, 'images': images})

    def post(self, request):
        nickname = request.POST.get('nickname', '')
        image = request.FILES.get('image')
        user = Profile.objects.get(id=request.user.id)
        user.nickname = nickname
        user.avatar = image
        user.save()
        messages.success(request, '修改成功！')
        return HttpResponseRedirect(reverse('user:center'))


class UserLike(View):
    def get(self, request, uid):
        articles = ArticleFollow.objects.filter(user_id=uid)
        paginator = Paginator(articles, 5)
        page = request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        topics = TopicFollow.objects.filter(user_id=uid)
        paginator = Paginator(topics, 5)
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)

        chats = ChatFollow.objects.filter(user_id=uid)
        paginator = Paginator(chats, 5)
        try:
            chats = paginator.page(page)
        except PageNotAnInteger:
            chats = paginator.page(1)
        except EmptyPage:
            chats = paginator.page(paginator.num_pages)

        images = ImageFollow.objects.filter(user_id=uid)
        paginator = Paginator(images, 5)
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
        return render(request, 'center-like.html',
                      {'articles': articles, 'topics': topics, 'chats': chats, 'images': images})


class MessageView(View):
    def get(self, request):
        news = Message.objects.filter(user=request.user).order_by("-create_time")
        paginator = Paginator(news, 5)
        page = request.GET.get('page')
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render(request, "message.html", {'news': news})

    def post(self, request):
        mid = request.POST.get('mid')
        Message.objects.get(id=mid).delete()
        return HttpResponseRedirect(reverse('user:message'))


class PasswordView(View):
    def get(self, request):
        return render(request, 'password.html')

    def post(self, request):
        oldpassword = request.POST.get('oldpwd')
        newpassword = request.POST.get('newpwd')
        retypepassword = request.POST.get('repwd')
        user = authenticate(username=request.user.email, password=oldpassword)
        if newpassword == retypepassword and user:
            user.password = make_password(newpassword)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            messages.error(request, '请确保两次密码相同且旧密码正确~')
            return render(request, 'password.html')


class SettingView(View):
    def get(self, request):
        return render(request, "setting.html")

    def post(self, request):
        nickname = request.POST.get('nickname')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        user = Profile.objects.get(id=request.user.id)
        user.nickname = nickname
        user.avatar = image
        user.location = location
        user.save()
        return HttpResponseRedirect(reverse('user:setting'))


class FindPasswordView(View):
    def get(self, request):
        return render(request, "repassword.html")

    def post(self, request):
        email = request.POST.get('email')
        try:
            Profile.objects.get(email=email)
            result = send_password_email(email=email)
            if result:
                # messages.success(request,'重置密码的链接已发送至你的邮箱，请注意查收~')
                return HttpResponse("重置密码的链接已发送至你的邮箱，请注意查收~")
            messages.error(request, '用户不存在~')
            return render(request, "repassword.html")
        except Profile.DoesNotExist:
            messages.error(request, '用户不存在~')
            return render(request, "repassword.html")


class SetPasswordView(View):
    def get(self, request):
        code = request.GET.get('code')
        return render(request, "setpassword.html", {'code': code})

    def post(self, request):
        code = request.POST.get('code')
        if code:
            password = request.POST.get('password')
            repassword = request.POST.get('repassword')
            if password == repassword:
                emailverity = EmailVerifyCode.objects.get(code=code)
                email = emailverity.email
                user = Profile.objects.get(email=email)
                user.password = make_password(password)
                user.save()
                emailverity.delete()
                return HttpResponseRedirect(reverse("user:login"))
        else:
            return render(request, "repassword.html")
