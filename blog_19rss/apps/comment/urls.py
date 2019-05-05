# -*- coding: utf-8 -*-
# @AuThor  : frank_lee
from django.conf.urls import url
from .views import AddcommentView

urlpatterns = [
    url(r'^add/$', AddcommentView, name='add_comment'),
]
