import xadmin
from xadmin import models
from .models import *
xadmin.autodiscover()



xadmin.site.register(Category)
xadmin.site.register(Topic)
xadmin.site.register(Article)
xadmin.site.register(Image)
xadmin.site.register(Chat)

xadmin.site.register(Contacts)

xadmin.site.register(ArticleComments)
xadmin.site.register(TopicComments)
xadmin.site.register(ChatComments)
xadmin.site.register(ImageComments)

xadmin.site.register(ArticleCommentReply)
xadmin.site.register(TopicCommentReply)
xadmin.site.register(ChatCommentReply)
xadmin.site.register(ImageCommentReply)


xadmin.site.register(CharReply)

xadmin.site.register(ArticleFollow)
xadmin.site.register(TopicFollow)
xadmin.site.register(ChatFollow)
xadmin.site.register(ImageFollow)


