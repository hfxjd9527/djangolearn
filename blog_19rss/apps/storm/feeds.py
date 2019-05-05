# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
from django.contrib.syndication.views import Feed
from django.conf import settings
from .models import Article


class AllArticleRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = settings.SITE_END_TITLE
    # 跳转网址，为主页
    link = '/'
    # 描述内容
    description = settings.SITE_DESCRIPTION

    # 需要显示的内容条目，这个可以挑选一些热门或者最新的博客
    def items(self):
        return Article.objects.all()[:100]

    # 显示内容的标题，这个才是最主要的东西
    def item_title(self, item):
        return "【{}】{}".format(item.category, item.title)

    # 显示内容的描述
    def item_description(self, item):
        return item.body_to_markdown()
