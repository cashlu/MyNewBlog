#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Cash on 2018/1/14
from django import template
from django.db.models import Count

from blog.models import Post, Category, Tag

# register引用为Library类的一个实例
register = template.Library()


# 最新文章的模板标签
# 装饰器的的作用，简单来说，就是将被装饰的函数，作为参数传入装饰函数，返回装饰函数的返回值。
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-created_time")[:num]


# dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，且是 Python 的
# date 对象，精确到月份，降序排列。接受的三个参数值表明了这些含义，一个是 created_time ，
# 即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排
# 在前面）。例如我们写了 3 篇文章，分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、
# 2017 年 3 月 28 日，那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间
# 列表，且降序排列，从而帮助我们实现按月归档的目的。
@register.simple_tag
def archives():
    # dates()方法返回一个list:
    # 第一个参数是字段名
    # 第二个参数是精度，必须是year/month/day其中之一
    # 第三个参数是排序，必须是ASC或者DESC其中之一
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.all()
    # 页面还要求得到每个分类下的文章的个数，其实可以用get_tags()同样的方法，但为了区分
    # 另外一种方法，这里没有使用，而是在页面用了{{ category.post_set.count }}。
    # 两种方法的效果是一样的。


@register.simple_tag
def get_tags():
    # 这里使用了django的Annotate，替代了all()方法，annotate不仅获取了Tags,还将每
    # 个tag关联的所有Post，还将所有Tag关联Post的数量，保存在num_posts变量中。
    # 后面的filter()，是筛选了所有关联Post数大于0的tags，不符合条件的过滤掉，不返回。
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    # 注意后面filter()中比较的语法。gt代表大于，=0代表大于的数字是0。这里有点儿特殊。
