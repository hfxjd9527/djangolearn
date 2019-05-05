"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from storm.sitemaps import ArticleSitemap, CategorySitemap, TagSitemap

# 网站地图
sitemaps = {
    'articles': ArticleSitemap,
    'tags': TagSitemap,
    'categories': CategorySitemap
}


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 用户
    url(r'^accounts/', include('user.urls', namespace='accounts')),
    # 评论
    url(r'^comment/', include('comment.urls', namespace='comment')),  # comment
    # storm 应用
    url('', include('storm.urls', namespace='blog')),
    # 网站地图
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
