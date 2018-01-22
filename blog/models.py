from django.contrib.auth.models import User
from django.db import models

# 模型必须继承models.Model类，类名就是表名。
# 文章的分类
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


class Category(models.Model):
    # 不需要创建ID字段，因为django会自动做这件事情。
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 文章的Tags
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 文章
class Post(models.Model):
    # 标题
    title = models.CharField(max_length=70)

    # 正文使用TextField()
    body = models.TextField()

    # 文章的创建时间和修改时间，用DateTimeField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要,也就是在文章列表中显示的文章的前200字，允许为空。
    excerpt = models.CharField(max_length=200, blank=True)

    # 文章的分类和标签，模型已经在上面定义了。
    # 文章与分类的关系是"一对多"关系（外键），一篇文章只能有一个分类，但是一个分类下可以有多篇文章。
    # 文章与标签的关系是"多对多"关系，一篇文章可以有多个标签，同样，一个标签也可以关联多篇文章。
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，
    # User 是 Django 为我们已经写好的用户模型。这里我们通过 ForeignKey 把文章和 User
    # 关联了起来。因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是
    # 一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 当文章的作者被删除时，作者的所有文章也级联删除。
    # 还可以有其他操作，比如留空，不变等等，可以查文档。

    # PositiveIntegerField类型值允许正整数或者0.
    views = models.PositiveIntegerField(default=0)

    # 注意，get_absolute_url()方法是页面调用！
    # 注意到 URL 配置中的 url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail') ，
    # 我们设定的 name='detail' 在这里派上了用场。看到这个 reverse 函数，它的第一个参数
    # 的值是 'blog:detail'，意思是 blog 应用下的 name=detail 的函数，由于我们在上面通过
    # app_name = 'blog' 告诉了 Django 这个 URL 模块是属于 blog 应用的，因此 Django
    # 能够顺利地找到 blog 应用下 name 为 detail 的视图函数，于是 reverse 函数会去解析
    # 这个视图函数对应的 URL，我们这里 detail 对应的规则就是 post/(?P<pk>[0-9]+)/
    # 这个正则表达式，而正则表达式部分会被后面传入的参数 pk 替换，所以，如果 Post 的 id
    # （或者 pk，这里 pk 和 id 是等价的） 是 255 的话，那么 get_absolute_url 函数返
    # 回的就是 /post/255/ ，这样 Post 自己就生成了自己的 URL。
    # 这里reverse()函数其实最终返回的是一个字符串，这个字符串就是这个Post对象的url。

    # get_absolute()这个方法的作用，简单来说，就是用自己的pk去替换url中的pk，获取自己的
    # url，然后url因为被点击了，所以会去调用views.detail()。
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 阅读了增加的方法。
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 重写save()方法，用于向数据库写入摘要。
    def save(self, *args, **kwargs):
        if not self.excerpt:
            # 实例化一个markdown对象，用于渲染body
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 1、先将Markdown文本渲染成HTML
            # 2、strip_tags()方法去掉HTML中的标签
            # 3、截取前54个字作为摘要
            self.excerpt = strip_tags(md.convert(self.body))[:200]

        # 调用父类save()方法，将数据保存到数据库。
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    # 在模型中定义，让Post按照时间来降序排列。
    class Meta:
        ordering = ['-created_time']
