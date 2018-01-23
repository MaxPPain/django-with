# coding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.func import rank_name

__all__ = [
    'Profile',
    'EmailVerifyCode',
    'Message'

]


class Profile(AbstractUser):
    class Meta:
        db_table = "w_users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    nickname = models.CharField('昵称', max_length=32, default=rank_name(6))
    avatar = models.ImageField('头像', upload_to="avatar/%Y/%m", default="avatar/avatar.jpg")
    intro = models.TextField('用户介绍', null=True, blank=True)
    veiwer = models.IntegerField('访客量', default=0, null=True, blank=True)
    location = models.CharField('地区', max_length=150, default="氪星")


    def __str__(self):
        return self.nickname

    def get_count(self):
        return self.user_article.count() + self.user_topic.count() + self.user_chat.count() + self.user_image.count()

    def get_like_count(self):
        return self.articlefollow_set.count() + self.topicfollow_set.count() + self.chatfollow_set.count() + self.imagefollow_set.count()


class EmailVerifyCode(models.Model):
    class Meta:
        db_table = "w_users_code"
        verbose_name = "用户邮箱确认码"
        verbose_name_plural = verbose_name

    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50)
    send_time = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    class Meta:
        db_table = "w_messages"
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    user = models.ForeignKey(Profile, verbose_name="所属用户")
    content = models.CharField('消息体', max_length=300)
    create_time = models.DateTimeField('时间', auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.content
