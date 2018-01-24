import markdown
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension

from blog.models import Post, Category, Tag
from comments.form import CommentForm


# 视图函数的方式
# def index(request):
#     # response = HttpResponse
#     # return response("hello")
#
#     # 返回的是一个HttpResponse的实例，传入的参数是一个字符串。
#     # 这里需要注意，Python没有new指令，在这里容易引起误解，return的不是一个类方法，
#     # 是一个实例方法。（理解的不一定正确，需要再查资料）
#     # return HttpResponse("欢迎访问我的部落格")
#
#     # 使用了模板，将context渲染到模板中。
#     # return render(request, 'blog/index.html',
#     #               context={
#     #                   'title': "Cash的部落格",
#     #                   'welcome': "欢迎来到我的部落格"
#     #               })
#
#     # 从数据库中取出所有的post，用创建时间倒序排列。
#     # post_list = Post.objects.all().order_by('-created_time')
#
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={'post_list': post_list})
# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     # 阅读量+1
#     post.increase_views()
#
#     # 将post.body做markdown渲染，就是将markdown格式转换为html格式。
#     # 这里需要注意的是，html页面中的标签，应该用{{post.body|safe}}
#     post.body = markdown(post.body,
#                          extensions=[
#                              'markdown.extensions.extra',
#                              'markdown.extensions.codehilite',
#                              'markdown.extensions.toc'
#                          ])
#
#     form = CommentForm()
#     # 因为detail页面有评论列表的显示，所以这里要获取评论列表，然后渲染给页面。
#     comment_list = post.comment_set.all()
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list
#                }
#
#     return render(request, 'blog/detail.html', context=context)
# 获取归档的文章列表（精度为月进行查找）
# todo 试一下用reverse()函数实现同样的功能。反过来也思考一下行不行。

# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     )
#     return render(request, 'blog/index.html', context={'post_list': post_list})


# 获取按照年月归档的文章
class PostArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'

    # 重写get_queryset()方法，并调用父类方法，加上filter实现。
    def get_queryset(self):
        return super(PostArchivesView, self).get_queryset().filter(
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
        )


# 搜索功能
# 搜索功能主要有两个功能点：
# 1. 通过表单获取到用户提交的搜索关键字，这里涉及到request的获取。用self.request。
# 2. 搜索本质上就是获取部分对象的结果集，所以在结果集的获取上，可以重写父类的get_queryset()
#       方法来解决，也就是get_queryset().filter()。
# 3. 如果页面不用HTML5，那么就必须判断用户输入的是否为空，如果为空，就不必再去数据库搜索，
#       直接给用户返回一个错误提示信息就可以。向模板的渲染，必须向context字典中加入一些
#       键值对。这就需要重写get_context_data()方法。其实本例中是不需要的，因为前端用
#       了HTML5。
# 这里是为了练手，自己实现了一个简单的全文检索功能。不过我们不用它，因为功能太简单了。而且
# 不支持索引，每次都是直接数据库查找，如果数据量大，或者请求量大，会有性能问题。也没有一些
# 复杂的功能，例如关键词高亮等，所以我们使用一个现成的第三方库：haystack
# class PostSearchResult(ListView):
#     """
#     全文检索功能。
#     """
#     model = Post
#     template_name = 'blog/index.html'
#     search_context = {}
#
#     def get_queryset(self):
#         q = self.request.GET.get('q')
#         if not q:
#             error_msg = '请输入关键字'
#             # 这个error_msg不是必须的，因为如果用HTML5的话，<input>标签有required属性，
#             # 代表表单要提交的话，这个<input>是必填项，所有就不用在代码中去判断是否为空了。
#             # 那么，整个这个类其实也就不用去重写get_context_data()方法了，因为重写这个
#             # 方法的目的就是为了把error_msg写进context中，以便传递给页面。
#
#             self.search_context['error_msg'] = error_msg
#             # 的东西：Q 对象。Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑。
#             # 例如这里 Q(title__icontains=q) | Q(body__icontains=q)
#             # 表示标题（title）含有关键词 q 或者正文（body）含有关键词 q ，
#             # 或逻辑使用 | 符号。如果不用 Q 对象，就只能写成
#             # title__icontains=q, body__icontains=q，
#             # 这就变成标题（title）含有关键词 q 且正文（body）含有关键词 q，
#             # 就达不到我们想要的目的。
#         return super().get_queryset().filter(
#             # 前缀 i 表示不区分大小写
#             Q(title__icontains=q) | Q(body__icontains=q)
#         )
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=object_list, **kwargs)
#         context.update(self.search_context)
#         return context


# 获取分类的文章列表
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     # post_list = Post.objects.filter(category=cate).order_by("-created_time")
#     post_list = Post.objects.filter(category=cate)
#
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(ListView):
    # 这个类视图的工作流程：
    # 1、定义 model = post，django 知道了要去取得所有Post模型的数据。
    # 2、定义 template_name = 'blog/index.html'，django 得知需要渲染哪个模板。
    # 3、定义 context_object_name = 'post_list'，django得知获取的Post列表保存
    #       在post_list中，context_object_name定义的是变量名，在html模板中获取
    #       模板变量时，就用这个名字。
    #
    # 使用类视图可以简化很多操作，好多工作 django 都替我们实现了。

    # 定义提取数据的模型。
    model = Post
    # 要渲染的目标模板
    template_name = 'blog/index.html'
    # 指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。
    context_object_name = 'post_list'
    # 每页显示的文章数
    paginate_by = 10

    def get_queryset(self):
        post_list = super().get_queryset()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite'
        ])
        for post in post_list:
            post.body = md.convert(post.body)
        return post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        # 视图中通过render()将一个字典context传递给模板，从而进行页面的渲染。而视图是通过
        # get_context_data()方法获取context的。这里重写这个方法，以便于可以在context
        # 字典中插入一些自定义的模板变量。

        # 先通过父类方法来获取基本的context数据。
        context = super().get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，
        # 此时 is_paginated=False。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据。
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
        if not is_paginated:
            return {}
        else:
            # 当前页左边连续的页码号，初始值为空。
            left = []
            # 当前页右边连续的页码号，初始值为空。
            right = []
            # 标示第 1 页页码后是否需要显示省略号。
            left_has_more = False
            # 标示最后一页页码前是否需要显示省略号。
            right_has_more = False

            # 标示是否需要显示第一页的页码.
            # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示
            # 第 1 页的页码号，其它情况下第一页的页码是始终需要显示的。
            # 初始值为 False
            first = False

            # 标示是否需要显示最后一页的页码号。
            last = False

            # 获取用户当前请求的页码
            page_number = page.number

            # 获取分页后的总页数
            total_pages = paginator.num_pages

            # 获取整个分页的页码列表
            page_range = paginator.page_range

            if page_number == 1:
                # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，
                # 因此 left=[]（已默认为空）。
                # 此时只要获取当前页右边的连续页码号,
                # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
                # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
                right = page_range[page_number: page_number + 2]

                # 如果最右边的页码号比最后一页的页码号减去 1 还要小，说明最右边的页码号
                # 和最后一页的页码号之间还有其它页码，因此需要显示省略号,
                # 通过 right_has_more 来指示。
                if right[-1] < total_pages - 1:
                    right_has_more = True

                # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中
                # 不包含最后一页的页码所以需要显示最后一页的页码号，通过 last 来指示。
                if right[-1] < total_pages:
                    last = True
            elif page_number == total_pages:
                # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，
                # 因此 right=[]（已默认为空），此时只要获取当前页左边的连续页码号。
                # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
                # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
                # TODO Lambda???
                left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

                # 如果最左边的页码号比第 2 页页码号还大，说明最左边的页码号和第 1 页的
                # 页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
                if left[0] > 2:
                    left_has_more = True

                # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中
                # 不包含第一页的页码，所以需要显示第一页的页码号，通过 first 来指示。
                if left[0] > 1:
                    first = True

            else:
                # 用户请求的既不是最后一页，也不是第一页，则需要获取当前页左右两边的连续页
                # 码号，这里只获取了当前页码前后连续两个页码，可以更改这个数字以获取更多页码。
                left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
                right = page_range[page_number:page_number + 2]
                # 是否需要显示最后一页和最后一页前的省略号
                if right[-1] < total_pages - 1:
                    right_has_more = True
                if right[-1] < total_pages:
                    last = True

                # 是否需要显示第 1 页和第 1 页后的省略号
                if left[0] > 2:
                    left_has_more = True
                if left[0] > 1:
                    first = True

            data = {
                'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last,
            }

            return data


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    # 重写父类的get_queryset()方法，因为该方法默认返回所有数据，而这里需要的是
    # 根据category分类筛选之后的。
    def get_queryset(self):
        # 在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，
        # 非命名组参数值保存在实例的 args 属性（是一个列表）里。所以我们使了
        # self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值。
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 小技巧：Pycharm的快捷键生成需要重写的方法，在super中加入这个类名和self就行。
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 因为文章详情页每被请求一次，该文章的浏览量就要+1，父类没有这个方法，我们在model
        # 中定义了increase()方法，所以要重写这个方法。
        self.object.increase_views()
        return response

        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post。

    def get_object(self, queryset=None):
        # 重写get_object()方法是因为要将post.body的markdown格式渲染成html格式。

        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            # 这里这样修改，是为了将TocExtension实例化，以便于传入slugify。
            # Markdown 内置的处理方法不能处理中文标题，所以我们使用了
            # django.utils.text 中的 slugify 方法，该方法可以很好地处理中文。
            # 效果就是点击目录后，定位到锚点后，浏览器地址栏显示的是中文锚点名称。
            TocExtension(slugify=slugify),

        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 重写get_context_data()的目的是，默认情况下，这个方法只是把post传递给模板。而在
        # Post的Detail页面，除了文章本身，还有评论表单，表单下面的评论列表，也需要传递给模
        # 板做渲染，所以这里重写这个方法，在context中把Post对象关联的comment_list也传递过去。

        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({'form': form,
                        'comment_list': comment_list
                        })
        return context


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
