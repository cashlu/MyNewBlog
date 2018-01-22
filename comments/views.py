from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post
from comments.form import CommentForm


def post_comment(request, post_pk):
    # 先获取被评论的Post，因为要和评论关联起来
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        # 用户提交的表单数据会封装在一个字典类中，通过request传递过来。CommentForm类接
        # 收字典后，会关联models.Comment定义的字段。
        # TODO 理解是否正确？
        form = CommentForm(request.POST)
        if form.is_valid():
            # 检查用户提交的数据是否合法，根据models.Comment中字段的数据类型判断。
            # TODO 理解是否正确？
            # 通过用户的表单数据，生成Comment类的实例，但是先不写入数据库，因为comment还
            # 有一个字段是Post的外键，下面需要先获取Post对象的id，然后一并写入数据库。
            comment = form.save(commit=False)
            comment.post = post
            # 写入数据库
            comment.save()
            # redirect()函数是重定向函数，当这个函数的参数是一个模型的实例时，
            # 则调用该模型的get_absolute_url()方法。
            # 这里的作用是，当用户提交评论后，需要返回detail页。当然，后续还需要对detail
            # 页做其他必要的数据处理和渲染，例如渲染所有的评论，包括最新的这一条。
            return redirect(post)
        else:
            # 如果检查到用户表单提交的数据不合法，则重新渲染detail页面，并且渲染表单的错误。
            # 所以这里我们需要传递三个模板变量给页面，一个是Post，一个是Comment_list，
            # 一个是表单form。

            # Post和Comment是外键关联，Comment中存储了Post的ID，
            # 所以post.comment_set()可以反向查询特定Post对应的所有Comment。
            # 等价于 Comment.objects.filter(post=post)
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            # 渲染detail页面，将context作为属性传递过去。
            return render(request, 'blog/detail.html', context=context)
    # 如果请求方法不是POST，则说面不是用户提交表单请求的页面，所以直接返回detail页面。
    return redirect(post)
