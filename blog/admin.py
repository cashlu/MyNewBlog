from django.contrib import admin

from blog.models import Post, Category, Tag


# 定义一个继承admin.ModelAdmin的子类，定义成员变量list_display，指定在后台列表中要显示
# 的字段，这些字段都是admin.site.register(Post, PostAdmin)中第一个参数的类变量。
# 所以要定义这个类，需要了解Post类中都有哪些类变量。
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time',
                    'category', 'author']


# 注册后台需要维护的Model
# register()函数的第二个参数是admin_class=None，这个类定义了在后台如何显示Post的信息。
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
