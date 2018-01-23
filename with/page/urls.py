# coding:utf-8
from django.conf.urls import url
from .views import *



urlpatterns = [

    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^article/$', ArticleView.as_view(), name='article'),
    url(r'^article/(?P<article_id>.*)$', ArticleDetailView.as_view(), name='article-detail'),

    #
    url(r'^topic/$', TopicView.as_view(), name='topic'),
    url(r'^topic/(?P<topic_id>.*)$', TopicDetailView.as_view(), name='topic-detail'),



    url(r'^chat/$', ChatView.as_view(), name='chat'),
    url(r'^chat/(?P<chat_id>.*)$', ChatDetailView.as_view(), name='chat-detail'),


    url(r'^image/$', ImageView.as_view(), name='image'),
    url(r'^image/(?P<img_id>.*)$', ImageDetailView.as_view(), name='image-detail'),


    url(r'^contact/$', ContactView.as_view(), name='contact'),

    url(r'^comment/id(\w+)comment_type(.+)/$', CommentView.as_view(), name='comment'),

    url(r'^reply/id(\w+)reply_type(.+)/$', ReplyView.as_view(), name='reply'),

    url(r'^api/reply/id(\w+)reply_type(.+)/$', LongReplyView.as_view(), name='areply'),


    url(r'^api/like/id(\w+)like_type(.+)/$', LikeView.as_view(), name='like'),
    url(r'^api/unlike/id(\w+)unlike_type(.+)/$', UnLikeView.as_view(), name='unlike'),


    url(r'^api/push/$', ArticlePushView.as_view(), name='push'),








    # url(r'^api/reply/id(\w+)reply_type(.+)/$', LongReplyView.as_view(), name='areply'),

]

# plist/p1(\w+)p2(.+)/