#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Cash on 2018/1/14
from django.conf.urls import url

from comments import views

app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$',
        views.post_comment,
        name='post_comment'),
]
