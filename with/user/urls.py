# coding:utf-8
from django.conf.urls import url
from .views import *

#注册，登录，登出

#个人中心设置包含 【设置个人信息、头像，密码，找回密码】

#个人：【我的文章，话题，闲聊，看图，】
#我的：【我的收藏】


urlpatterns = [

    url(r'^register/$', RegisterView.as_view(), name="register"),                   #注册
    url(r'^login/$', LoginView.as_view(), name="login"),                            #登录
    url(r'^logout/$', LogoutView.as_view(), name="logout"),                         #登出
    url(r'^user/(?P<uid>\d+)/$', CenterView.as_view(), name="center"),              #个人中心
    url(r'^user/like/(?P<uid>\d+)/$', UserLike.as_view(), name="user-like"),              #用户喜欢

    url(r'^message/$', MessageView.as_view(), name="message"),
    url(r'^setting/$', SettingView.as_view(), name='setting'),


    url(r'^password/$', PasswordView.as_view(), name="password"),
    url(r'^setpassword/', SetPasswordView.as_view(), name="setpassword"),
    url(r'^find_password/$', FindPasswordView.as_view(), name="find_pass"),                              #找回密码


]