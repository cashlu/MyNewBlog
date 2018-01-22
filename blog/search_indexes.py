#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Cash on 2018/1/16


from haystack import indexes

from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # 如果使用一个字段设置了document=True，则一般约定此字段名为text，
    # 这是在 SearchIndex 类里面一贯的命名
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
    # 这是 django haystack 的规定。要相对某个 app 下的数据进行全文检索，就要在
    # 该 app 下创建一个 search_indexes.py 文件，然后创建一个 XXIndex 类
    # （XX 为含有被检索数据的模型，如这里的 Post），并且继承 SearchIndex 和 Indexable。
