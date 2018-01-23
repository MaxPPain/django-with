# coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from . import settings
import xadmin
from xadmin.plugins import xversion

xversion.register_models()

xadmin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('page.urls', namespace='page')),
    url(r'^', include('user.urls', namespace='user')),
    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),


    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]