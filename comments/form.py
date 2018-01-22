#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Cash on 2018/1/14

from django import forms

from comments.models import Comment


# todo 需要仔细了解一下django的表单类
# 使用 django 的表单功能，需要创建一个表单类，继承 forms.ModelForm 类。
# django可以自动的完成一些表单的功能。只需要几个步骤：
# 1、创建表单所需字段表结构的model。
# 2、创建一个继承 forms.ModelForm 的表单类。
# 3、类中指定model和fields
class CommentForm(forms.ModelForm):
    class Meta:
        # 评论表单的数据模型是models.Comment类
        model = Comment
        # 需要显示的字段有如下几个
        fields = ['name', 'email', 'url', 'text']
