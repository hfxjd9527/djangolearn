# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
from django.conf.urls import url
from .views import IndexView, DetailView, MessageView, AboutView, DonateView, ExchangeView

urlpatterns = [
    # 首页
    url(r'^$', IndexView.as_view(template_name='index.html'), name='index'),
    # 给我留言
    url(r'^category/message/$', MessageView, name='message'),
    # 关于自己
    url(r'^category/about/$', AboutView, name='about'),
    # 赞助作者
    url(r'^category/donate/$', DonateView, name='donate'),
    # 技术交流
    url(r'^category/exchange/$', ExchangeView, name='exchange'),
    # 分类页面
    url(r'^category/(?P<bigslug>.*?)/(?P<slug>.*?)', IndexView.as_view(template_name='content.html'), name='category'),
    # 归档页面
    url(r'^date/(?P<year>\d+)/(?P<month>\d+)/$', IndexView.as_view(template_name='archive.html'), name='date'),
    # 标签页面
    url(r'^tag/(?P<tag>.*?)/$', IndexView.as_view(template_name='content.html'), name='tag'),
    # 文章详情页
    url(r'^article/(?P<slug>.*?)/$', DetailView, name='article')
]
