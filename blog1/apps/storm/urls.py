# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
from django.conf.urls import url
from .views import IndexView, MessageView, AboutView, DonateView, ExchangeView

urlpatterns = [
    url(r'^$', IndexView.as_view(template_name='index.html'), name='index'),
    url(r'^category/(?P<bigslug>.*?)/(?P<slug>.*?)', IndexView.as_view(template_name='content.html'), name='category'),
    url(r'^category/message/$', MessageView, name='message'),
    url(r'^category/about/$', AboutView, name='about'),
    url(r'^category/donate/$', DonateView, name='donate'),
    url(r'^category/exchange/$', ExchangeView, name='exchange'),
    # 归档页面
    url(r'^date/(?P<year>\d+)/(?P<month>\d+)/$', IndexView.as_view(template_name='archive.html'), name='date'),
    # 标签页面
    url(r'^tag/(?P<tag>.*?)/$', IndexView.as_view(template_name='content.html'), name='tag'),
]
