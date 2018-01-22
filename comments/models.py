from django.db import models


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    # 添加日期数据库自动写入，因为不希望用户自己填时间。
    created_time = models.DateTimeField(auto_now_add=True)
    # Comment必须和Post关联，一个Post可以有多个Comment，是"一对多关系"，所以用外键。
    # 每个Comment保存一个Post的ID，从而能确定这个Comment是哪一个Post的评论。
    # 这种"一对多关系"，是在"多"这方的表中维护"一"一方的ID作为外键。
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    # 当评论关联的外键对象，也就是Post本身被删除时，评论也级联删除

    def __str__(self):
        return self.text[:20]
