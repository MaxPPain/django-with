# coding:utf-8
import datetime
import json
import os
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .forms import *
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from utils.func import getsalt
from user.models import Message

__all__ = [
    'IndexView',

    'ArticleView',
    'ArticleDetailView',

    'TopicView',
    'TopicDetailView',

    'ChatView',
    'ChatDetailView',

    'ImageView',
    'ImageDetailView',

    'ContactView',
    'CommentView',
    'ReplyView',
    'LongReplyView',

    'LikeView',
    'UnLikeView',
    'ArticlePushView',

]


# home
class IndexView(View):
    def get(self, request):
        chats = Chat.objects.all()[:4]
        articles = Article.objects.all()[:4]
        topics = Topic.objects.all()[:4]
        images = Image.objects.all()[:4]
        return render(request, "home.html", {'topics': topics, 'articles': articles, 'chats': chats, 'images': images})


class ArticleView(View):
    def get(self, request):
        articles = Article.objects.all().order_by("-create_time")
        search = request.GET.get('search')
        if search:
            articles = articles.filter(
                Q(title__icontains=search) | Q(content__icontains=search) | Q(user__nickname=search))
        paginator = Paginator(articles, 4)
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return render(request, "article.html", {'articles': articles})


class ArticleDetailView(View):
    def get(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
            article.read_count += 1
            article.save()
            comments = ArticleComments.objects.filter(article_id=article_id)
            return render(request, 'article-detail.html',
                          {'article': article, 'comments': comments})
        except Article.DoesNotExist:
            return HttpResponse('404', staus=404)


# 话题
class TopicView(View):
    def get(self, request):
        topics = Topic.objects.all().order_by("-create_time")
        search = request.GET.get('search')
        if search:
            topics = topics.filter(Q(content__icontains=search) | Q(user__nickname=search))
        paginator = Paginator(topics, 5)
        page = request.GET.get('page')
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)
        return render(request, "topic.html", {'topics': topics})

    def post(self, request):
        content = request.POST.get('topic')
        Topic.objects.create(content=content, user_id=request.user.id)
        return HttpResponseRedirect(reverse('page:topic'))


class TopicDetailView(View):
    def get(self, request, topic_id):
        try:
            topic = Topic.objects.get(id=topic_id)
            topic.read_count += 1
            topic.save()
            comments = TopicComments.objects.filter(topic=topic_id)
            return render(request, 'topic-detail.html',
                          {'topic': topic, 'comments': comments})
        except Topic.DoesNotExist:
            return HttpResponse('404', status=404)


# 闲聊
class ChatView(View):
    def get(self, request):
        chats = Chat.objects.all().order_by('create_time')
        search = request.GET.get('search')
        if search:
            chats = chats.filter(Q(content__icontains=search) | Q(user__nickname=search))
        paginator = Paginator(chats, 4)
        page = request.GET.get('page')
        try:
            chats = paginator.page(page)
        except PageNotAnInteger:
            chats = paginator.page(1)
        except EmptyPage:
            chats = paginator.page(paginator.num_pages)
        return render(request, "chat.html", {'chats': chats})

    def post(self, request):
        content = request.POST.get('chat')
        Chat.objects.create(content=content, user_id=request.user.id)
        return HttpResponseRedirect(reverse('page:chat'))


class ChatDetailView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            chat.read_count += 1
            chat.save()
            return render(request, 'chat-detail.html',
                          {'chat': chat})
        except Chat.DoesNotExist:
            return HttpResponse('404', status=404)


# 发布
class ImageView(View):
    def get(self, request):
        images = Image.objects.all().order_by("-create_time")
        search = request.GET.get('search')
        if search:
            images = images.filter(Q(title__icontains=search) | Q(user__nickname=search))
        paginator = Paginator(images, 4)
        page = request.GET.get('page')
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
        return render(request, "image.html", {'images': images})

    def post(self, request):
        title = request.POST.get('title')
        image = request.FILES.get('image')
        images = Image(title=title, url=image, user_id=request.user.id)
        images.save()
        return HttpResponseRedirect(reverse('page:image'))


# 图片详情
class ImageDetailView(View):
    def get(self, request, img_id):
        try:
            image = Image.objects.get(id=int(img_id))
            image.read_count += 1
            image.save()
            comments = ImageComments.objects.filter(image_id=image.id)
            return render(request, 'image-detail.html',
                          {'image': image, 'comments': comments})
        except Image.DoesNotExist:
            return HttpResponse('404', status=404)


class CommentView(View):
    def post(self, request, aid, comment_type):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = request.POST.get('content')
            if comment_type == "1":
                ArticleComments.objects.create(content=content, article_id=int(aid), user=request.user)
                return HttpResponseRedirect(reverse('page:article-detail', args=aid))
            elif comment_type == "2":
                TopicComments.objects.create(content=content, topic_id=int(aid), user=request.user)
                return HttpResponseRedirect(reverse('page:topic-detail', args=aid))
            elif comment_type == "3":
                ChatComments.objects.create(content=content, chat_id=int(aid), user=request.user)
                return HttpResponseRedirect(reverse('page:chat-detail', args=aid))
            else:
                ImageComments.objects.create(content=content, image_id=int(aid), user=request.user)
                return HttpResponseRedirect(reverse('page:image-detail', args=aid))
        else:
            messages.error(request, "超过字数限制了！")
            if comment_type == "1":
                return HttpResponseRedirect(reverse('page:article-detail', args=aid))
            elif comment_type == "2":
                return HttpResponseRedirect(reverse('page:topic-detail', args=aid))
            elif comment_type == "3":
                return HttpResponseRedirect(reverse('page:chat-detail', args=aid))
            else:
                return HttpResponseRedirect(reverse('page:image-detail', args=aid))


class ReplyView(View):
    def post(self, request, aid, reply_type):
        content = request.POST.get('replycontent')
        if reply_type == "1":
            ArticleCommentReply.objects.create(content=content, reply_id=int(aid), user=request.user)
            id = ArticleComments.objects.get(id=int(aid)).article.id
            return HttpResponseRedirect(reverse('page:article-detail', args=str(id)))
        elif reply_type == "2":
            TopicCommentReply.objects.create(content=content, reply_id=int(aid), user=request.user)
            id = TopicComments.objects.get(id=int(aid)).topic.id
            return HttpResponseRedirect(reverse('page:topic-detail', args=str(id)))
        elif reply_type == "3":
            ChatCommentReply.objects.create(content=content, reply_id=int(aid), user=request.user)
            id = ChatComments.objects.get(id=int(aid)).chat.id
            return HttpResponseRedirect(reverse('page:chat-detail', args=str(id)))
        else:
            ImageCommentReply.objects.create(content=content, reply_id=int(aid), user=request.user)
            id = ImageComments.objects.get(id=int(aid)).image.id
            return HttpResponseRedirect(reverse('page:image-detail', args=str(id)))


class LongReplyView(View):
    def post(self, request, aid, reply_type):
        content = request.POST.get('replycontent')
        if reply_type == "1":
            ArticleReply.objects.create(content=content, articlereply_id=int(aid), user=request.user)
            id = ArticleCommentReply.objects.get(id=int(aid)).reply.article.id
            return HttpResponseRedirect(reverse('page:article-detail', args=str(id)))
        elif reply_type == "2":
            TopicReply.objects.create(content=content, topicreply_id=int(aid), user=request.user)
            id = TopicCommentReply.objects.get(id=int(aid)).reply.topic.id
            return HttpResponseRedirect(reverse('page:topic-detail', args=str(id)))
        elif reply_type == "3":
            CharReply.objects.create(content=content, chatreply_id=int(aid), user=request.user)
            id = ChatCommentReply.objects.get(id=int(aid)).reply.chat.id
            return HttpResponseRedirect(reverse('page:chat-detail', args=str(id)))
        else:
            ImageReply.objects.create(content=content, imagereply_id=int(aid), user=request.user)
            id = ImageCommentReply.objects.get(id=int(aid)).reply.image.id
            return HttpResponseRedirect(reverse('page:image-detail', args=str(id)))


# 联系我们
class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")

    def post(self, request):
        name = request.POST.get('contact_name')
        email = request.POST.get('contact_email')
        message = request.POST.get('contact_message')
        messages.success(request, '谢谢给我们提供宝贵的意见，感谢您的支持')
        Contacts.objects.create(username=name, email=email, content=message)
        return HttpResponseRedirect(reverse("page:index"))


class LikeView(View):
    def post(self, request, aid, like_type):
        if like_type == "1":
            try:
                ArticleFollow.objects.get(article_id=int(aid),user=request.user)
                messages.error(request, '已经喜欢我啦~~~！')
                return HttpResponseRedirect(reverse('page:article'))
            except ObjectDoesNotExist:
                like = ArticleFollow.objects.create(article_id=int(aid), user=request.user)
                article = Article.objects.get(id=like.article_id)
                article.like_count += 1
                Message.objects.create(
                    content=request.user.nickname + "收藏了你的文章" + '<a href="/article/"' + str(article.id) + ">点我查看详情</a>",
                    status=0,
                    user_id=article.user.id)
                article.save()
                messages.success(request, "感谢你的喜欢！")
                return HttpResponseRedirect(reverse('page:article'))
        elif like_type == "2":
            try:
                TopicFollow.objects.get(topic_id=int(aid),user=request.user)
                messages.error(request, '已经喜欢我啦~~~！')
                return HttpResponseRedirect(reverse('page:topic'))
            except ObjectDoesNotExist:
                like = TopicFollow.objects.create(topic_id=int(aid), user=request.user)
                topic = Topic.objects.get(id=like.topic_id)
                topic.like_count += 1
                Message.objects.create(
                    content=request.user.nickname + "收藏了你的话题" + '<a href="/topic/"' + str(topic.id) + ">点我查看详情</a>",
                    status=0,
                    user_id=topic.user.id)
                topic.save()
                messages.success(request, "感谢你的喜欢！")
                return HttpResponseRedirect(reverse('page:topic'))
        elif like_type == "3":
            try:
                ChatFollow.objects.get(chat_id=int(aid),user=request.user)
                messages.error(request, '已经喜欢我啦~~~！')
                return HttpResponseRedirect(reverse('page:chat'))
            except ObjectDoesNotExist:
                like = ChatFollow.objects.create(chat_id=int(aid), user=request.user)
                chat = Chat.objects.get(id=like.chat_id)
                chat.like_count += 1
                Message.objects.create(
                    content=request.user.nickname + "收藏了你的闲聊" + '<a href="/chat/"' + str(chat.id) + ">点我查看详情</a>",
                    status=0,
                    user_id=chat.user.id)
                chat.save()
                messages.success(request, "感谢你的喜欢！")
                return HttpResponseRedirect(reverse('page:chat'))
        else:
            try:
                ImageFollow.objects.get(image_id=int(aid),user=request.user)
                messages.error(request, '已经喜欢我啦~~~！')
                return HttpResponseRedirect(reverse('page:image'))
            except ObjectDoesNotExist:
                like = ImageFollow.objects.create(image_id=int(aid), user=request.user)
                image = Image.objects.get(id=like.image_id)
                image.like_count += 1
                Message.objects.create(
                    content=request.user.nickname + "收藏了你的图片" + '<a href="/image/"' + str(image.id) + ">点我查看详情</a>",
                    status=0,
                    user_id=image.user.id)
                image.save()
                messages.success(request, "感谢你的喜欢！")
                return HttpResponseRedirect(reverse('page:image'))


class UnLikeView(View):
    def post(self, request, aid, unlike_type):
        if unlike_type == "1":
            like = ArticleFollow.objects.get(article_id=int(aid), user=request.user)
            article = Article.objects.get(id=like.article_id)
            if article.like_count == 1:
                article.like_count = 1
            else:
                article.like_count -= 1
            article.save()
            like.delete()
        elif unlike_type == "2":
            like = TopicFollow.objects.get(topic_id=int(aid), user=request.user)
            topic = Topic.objects.get(id=like.topic_id)
            if topic.like_count == 1:
                topic.like_count = 1
            else:
                topic.like_count -= 1
            topic.save()
            like.delete()
        elif unlike_type == "3":
            like = ChatFollow.objects.get(chat_id=int(aid), user=request.user)
            chat = Chat.objects.get(id=like.chat_id)
            if chat.like_count == 1:
                chat.like_count = 1
            else:
                chat.like_count -= 1
            chat.save()
            like.delete()
        else:
            like = ImageFollow.objects.get(image_id=int(aid), user=request.user)
            image = Image.objects.get(id=like.image_id)
            if image.like_count == 1:
                image.like_count = 1
            else:
                image.like_count -= 1
            image.save()
            like.delete()
        return HttpResponseRedirect(reverse('user:user-like', args=str(request.user.id)))


class ArticlePushView(View):
    def get(self, request):
        def get_object(request):
            r = [('', '----')]
            for obj in Category.objects.all():
                r = r + [(obj.id, obj.name)]
            return r

        form = ArticleForm()
        form.fields['category'].choices = get_object(request)
        return render(request, "push.html", {'form': form})

    def post(self, request):
        image = request.FILES.get('image')
        name = request.POST.get('name')
        category = request.POST.get('category')
        content = request.POST.get('content')
        Article.objects.create(title=name, image=image, content=content, category_id=category, user=request.user)
        return HttpResponseRedirect(reverse('page:article'))
