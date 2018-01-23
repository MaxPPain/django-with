# coding:utf-8
from django.db import models
from user.models import *
from ckeditor_uploader.fields import RichTextUploadingField

__all__ = [
    'Category',
    'Topic',
    'Article',
    'Chat',
    'Image',
    'Contacts',
    'ArticleComments',
    'TopicComments',
    'ChatComments',
    'ImageComments',
    'ArticleCommentReply',
    'TopicCommentReply',
    'ChatCommentReply',
    'ImageCommentReply',
    'ArticleFollow',
    'TopicFollow',
    'ChatFollow',
    'ImageFollow',
    'CharReply',
    'ImageReply',
    'ArticleReply',
    'TopicReply',
]

'''分类'''


class Category(models.Model):
    class Meta:
        db_table = "categories"
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    name = models.CharField('名称', max_length=255)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    '''文章'''

    class Meta:
        db_table = "articles"
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    title = models.CharField('文章名称', max_length=255)
    image = models.ImageField("封面", upload_to="article/%Y/%m")
    content = RichTextUploadingField('内容', config_name="basic")
    like_count = models.IntegerField('喜欢数', default=0, null=True, blank=True)
    read_count = models.IntegerField('阅读数', default=0, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, related_name='user_article', verbose_name='所属用户')
    category = models.ForeignKey(Category, verbose_name='所属分类')

    def __str__(self):
        return self.title


    # 获取同分类的文章数量
    def get_categories(self):
        return Article.objects.filter(pk=self.category.id).count()

    # 获取文章数量
    def get_article_count(self):
        return Article.objects.all().count()

    # 获取最新文章评论
    def get_last_comment(self):
        return self.articlecomments_set.last("-id").content


class ArticleComments(models.Model):
    class Meta:
        db_table = "article_comments"
        verbose_name = '文章评论'
        verbose_name_plural = verbose_name

    content = models.TextField("内容")
    user = models.ForeignKey(Profile, related_name='user_a_comments', verbose_name='所属用户')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    article = models.ForeignKey(Article, verbose_name="评论所属文章")

    def __str__(self):
        return self.content

    def get_reply(self):
        return ArticleCommentReply.objects.filter(reply=self.pk)


class Topic(models.Model):
    '''话题'''

    class Meta:
        db_table = "topics"
        verbose_name = '话题'
        verbose_name_plural = verbose_name

    content = models.TextField('话题')
    like_count = models.IntegerField('喜欢数', default=0, null=True, blank=True)
    read_count = models.IntegerField('阅读数', default=0, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, related_name='user_topic', verbose_name='所属用户')

    def __str__(self):
        return self.content

    def get_topic_count(self):
        return Topic.objects.all().count()

    def get_last_comment(self):
        return self.topiccomments_set.latest("-id").content

    def get_comment_num(self):
        return self.topiccomments_set.count()



class TopicComments(models.Model):
    class Meta:
        db_table = "topic_comments"
        verbose_name = '话题评论'
        verbose_name_plural = verbose_name

    content = models.TextField("内容")
    user = models.ForeignKey(Profile, related_name='user_t_comments', verbose_name='所属用户')
    topic = models.ForeignKey(Topic, verbose_name="评论所属话题")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.content

    def get_reply(self):
        return TopicCommentReply.objects.filter(reply=self.pk)


class Chat(models.Model):
    '''闲聊'''

    class Meta:
        db_table = "chats"
        verbose_name = '闲聊'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    content = models.TextField('内容', max_length=255)
    like_count = models.PositiveIntegerField('喜欢数', default=0, null=True, blank=True)
    read_count = models.PositiveIntegerField('阅读数', default=0, null=True, blank=True)
    user = models.ForeignKey(Profile, related_name='user_chat', verbose_name='所属用户')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.content

    def get_comment_num(self):
        return ChatComments.objects.all().count()


    def get_last_comment(self):
        return self.chatcomments_set.latest("-id").content

    def get_comment(self):
        return ChatComments.objects.filter(chat_id=self.pk)

    def get_one_comment(self):
        return ChatComments.objects.filter(chat_id=self.pk)[:1]





class ChatComments(models.Model):
    class Meta:
        db_table = "chat_comments"
        verbose_name = '闲聊评论'
        verbose_name_plural = verbose_name

    content = models.TextField("内容")
    chat = models.ForeignKey(Chat, verbose_name="评论所属闲聊")
    user = models.ForeignKey(Profile, related_name='user_c_comments', verbose_name='所属用户')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.content


    def get_reply(self):
        return ChatCommentReply.objects.filter(reply=self.pk)

    def get_one_reply(self):
        return ChatCommentReply.objects.filter(reply=self.pk)[:1]


class Image(models.Model):
    '''看图'''
    class Meta:
        db_table = "images"
        verbose_name = '看图'
        verbose_name_plural = verbose_name

    title = models.CharField('寓意', max_length=50, null=True, blank=True)
    url = models.ImageField("封面", upload_to="images/%Y/%m")
    like_count = models.PositiveIntegerField('喜欢数', default=0, null=True, blank=True)
    read_count = models.PositiveIntegerField('阅读数', default=0, null=True, blank=True)
    user = models.ForeignKey(Profile, related_name='user_image', verbose_name='所属用户')
    create_time = models.DateTimeField('创建时间', auto_now=True)

    def __str__(self):
        return "%s" %self.id

    def get_image_count(self):
        return Image.objects.all().count()

    def get_last_comment(self):
        return self.imagecomments_set.latest("-id").content

    def get_comment_num(self):
        return self.imagecomments_set.count()


class ImageComments(models.Model):
    class Meta:
        db_table = "image_comments"
        verbose_name = '看图评论'
        verbose_name_plural = verbose_name

    content = models.TextField("内容")
    image = models.ForeignKey(Image, verbose_name="评论所属看图")
    user = models.ForeignKey(Profile, related_name='user_i_comments', verbose_name='所属用户')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.content


    def get_reply(self):
        return ImageCommentReply.objects.filter(reply=self.pk)


class Contacts(models.Model):
    '''联系我们'''

    class Meta:
        db_table = "contacts"
        verbose_name = '意见'
        verbose_name_plural = verbose_name

    username = models.CharField('用户名', max_length=150)
    email = models.EmailField()
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username





class ArticleCommentReply(models.Model):
    class Meta:
        db_table = "article_comments_reply"
        verbose_name = '文章评论回复'
        verbose_name_plural = verbose_name

    content = models.TextField('回复内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, verbose_name='所属用户')
    reply = models.ForeignKey(ArticleComments)

    def __str__(self):
        return "回复的内容:" + self.content + "-------评论内容:" + self.reply.content


    def get_replys(self):
        return ArticleReply.objects.filter(articlereply=self.pk)


class TopicCommentReply(models.Model):
    class Meta:
        db_table = "topic_comments_reply"
        verbose_name = '话题评论回复'
        verbose_name_plural = verbose_name

    content = models.TextField('回复内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, verbose_name='所属用户')
    reply = models.ForeignKey(TopicComments)

    def __str__(self):
        return "回复的内容:" + self.content + "-------评论内容:" + self.reply.content


    def get_replys(self):
        return TopicReply.objects.filter(topicereply=self.pk)


class ChatCommentReply(models.Model):
    class Meta:
        db_table = "chat_comments_reply"
        verbose_name = '闲聊评论回复'
        verbose_name_plural = verbose_name

    content = models.TextField('回复内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, verbose_name='所属用户')
    reply = models.ForeignKey(ChatComments)

    def __str__(self):
        return "评论回复的内容:" + self.content + "-------评论内容:" + self.reply.content

    def get_replys(self):
        return CharReply.objects.filter(chatreply=self.pk)




class ImageCommentReply(models.Model):
    class Meta:
        db_table = "image_comments_reply"
        verbose_name = '看图评论回复'
        verbose_name_plural = verbose_name

    content = models.TextField('回复内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, verbose_name='所属用户')
    reply = models.ForeignKey(ImageComments)

    def __str__(self):
        return "回复的内容:" + self.content


    def get_replys(self):
        return ImageReply.objects.filter(imagereply=self.pk)



class CharReply(models.Model):
    class Meta:
        db_table = "chat_reply"
        verbose_name = '闲聊回复'
        verbose_name_plural = verbose_name

    content = models.TextField('回复内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, verbose_name='所属用户')
    chatreply = models.ForeignKey(ChatCommentReply)

    def __str__(self):
        return "评论回复内容:" + self.chatreply.content



class ArticleReply(models.Model):
    class Meta:
        db_table = "article_reply"
        verbose_name = '文章回复'
        verbose_name_plural = verbose_name

    content = models.TextField('回复内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, verbose_name='所属用户')
    articlereply = models.ForeignKey(ArticleCommentReply)

    def __str__(self):
        return "评论回复内容:" + self.articlereply.content


class TopicReply(models.Model):
    class Meta:
        db_table = "topic_reply"
        verbose_name = '话题回复'
        verbose_name_plural = verbose_name

    content = models.TextField('回复内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, verbose_name='所属用户')
    topicreply = models.ForeignKey(TopicCommentReply)

    def __str__(self):
        return "评论回复内容:" + self.topicreply.content


class ImageReply(models.Model):
    class Meta:
        db_table = "image_reply"
        verbose_name = '闲聊回复'
        verbose_name_plural = verbose_name

    content = models.TextField('回复内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(Profile, verbose_name='所属用户')
    imagereply = models.ForeignKey(ImageCommentReply)

    def __str__(self):
        return "评论回复内容:" + self.imagereply.content


class ArticleFollow(models.Model):
    class Meta:
        db_table = "w_article_follow"
        verbose_name = "用户文章收藏"
        verbose_name_plural = verbose_name

    user = models.ForeignKey(Profile)
    article = models.ForeignKey(Article)
    create_time = models.DateTimeField('时间', auto_now_add=True)

    def __str__(self):
        return self.article.title


class TopicFollow(models.Model):
    class Meta:
        db_table = "w_topic_follow"
        verbose_name = "用户话题收藏"
        verbose_name_plural = verbose_name

    user = models.ForeignKey(Profile)
    topic = models.ForeignKey(Topic)
    create_time = models.DateTimeField('时间', auto_now_add=True)

    def __str__(self):
        return self.topic.content


class ChatFollow(models.Model):
    class Meta:
        db_table = "w_chat_follow"
        verbose_name = "用户闲聊收藏"
        verbose_name_plural = verbose_name

    user = models.ForeignKey(Profile)
    chat = models.ForeignKey(Chat)
    create_time = models.DateTimeField('时间', auto_now_add=True)

    def __str__(self):
        return self.chat.content


class ImageFollow(models.Model):
    class Meta:
        db_table = "w_image_follow"
        verbose_name = "用户看图收藏"
        verbose_name_plural = verbose_name

    user = models.ForeignKey(Profile)
    image = models.ForeignKey(Image)
    create_time = models.DateTimeField('时间', auto_now_add=True)

    def __str__(self):
        return "%s" % self.image.id
