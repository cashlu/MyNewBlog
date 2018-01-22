#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Cash on 2018/1/16
from django.contrib.syndication.views import Feed

from blog.models import Post

'''
用于RSS阅读器的订阅。
'''


class AllPostsFeed(Feed):
    # 显示在RSS阅读器上的标题
    title = 'Cash的部落格'

    # 通过阅读器跳转到网页的地址
    link = '/'

    description = "这里是描述信息"

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # RSS阅览器显示的内容的描述
    def item_description(self, item):
        return item.body
