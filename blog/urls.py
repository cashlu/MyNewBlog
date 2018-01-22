#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Cash on 2018/1/13


from django.conf.urls import url

from . import views, feeds

# 视图函数命名空间
# 告诉 Django 这个 urls.py 模块是属于 blog 应用的。我们看到 blog\urls.py 目前有两个
# 视图函数，并且通过 name 属性给这些视图函数取了个别名，分别是 index、detail。但是一个复
# 杂的 Django 项目可能不止这些视图函数，例如一些第三方应用中也可能有叫 index、detail 的
# 视图函数，那么怎么把它们区分开来，防止冲突呢？方法就是通过 app_name 来指定命名空间。
app_name = 'blog'

urlpatterns = [
    # 第一个参数是请求的网址
    # 第二个参数是处理该请求的函数
    # 第三个参数是该函数的别名
    # url(r'^$', views.index, name='index'),

    # 使用类视图，这里需要调用as_view方法，因为，url需要绑定的是一个视图函数，而IndexView
    # 是一个类，所以调用这个方法，将他转换成一个函数。
    url(r'^$', views.IndexView.as_view(), name='index'),

    # ?P<pk>[0-9]+ 是命名捕获组，代表将0-9的任意位数字，赋值给pk，然后将pk作为参数，
    # 传递给要调用的 views ,在本例中，相当于 views.detail(request, pk=132) ,作用是
    # 我们需要从url的调用中得知，用户要访问的文章的 pk ，以便于程序在数据库中找到这篇文章
    # 并显示出来。

    # 这里其实有更复杂的工作机制，在model.Post中，定义了get_absolute_url()方法，该方法
    # 将自己的pk值，"解析"回blog:detail这个url(name="detail")，替换了"命名捕获组"——pk，
    # 页面中文章标题或者"继续阅读"链接，会调用Post对象的get_absolute_url()方法，该方法解析
    # 到对应的url，替换pk后，url又调用views.detail()函数，将pk作为参数传递过去，
    # 获取了对应的Post对象，然后向页面渲染。
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(),
        name="detail"),

    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',
        views.PostArchivesView.as_view(),
        name='archives'),

    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(),
        name="category"),

    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),

    # 由于AllPostFeed继承自Feed，这里不需要调用as_views()，需要注意。
    url(r'^all/rss/$', feeds.AllPostsFeed(), name='rss'),

    # 这个url是给自己实现的那个简单的全文检索用的，因为使用了haystack，所以这里要注释掉。
    # url(r'^search/$', views.PostSearchResult.as_view(), name='search'),
]
