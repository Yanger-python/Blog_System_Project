from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
# Create your models here.


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )
    WEIGHT_ITEMS = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接")  # 默认长度为200
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    weight = models.PositiveIntegerField(default=1, choices=WEIGHT_ITEMS, verbose_name="权重",
                                         help_text="权重高展示顺序靠前")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "友链"


class SlideBar(models.Model):

    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4

    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, "展示"),
        (STATUS_HIDE, "隐藏"),
    )
    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMENT, '最近评论'),
    )
    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name="展示类型")
    context = models.CharField(max_length=500, blank=True, verbose_name="侧边栏内容", help_text="如果设置的不是html类型，可为空")
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        from django_blog_app.models import Post
        from comment.models import Comment

        result = ""
        if self.display_type == self.DISPLAY_HTML:
            result = self.context
        elif self.display_type == self.DISPLAY_LATEST:
            context = {'posts': Post.latest_posts()[:3]}
            result = render_to_string('config_app/sidebar_post_list.html', context=context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {'posts': Post.hot_post()[:5]}
            result = render_to_string('config_app/sidebar_post_list.html', context=context)
        elif self.display_type == self.DISPLAY_COMMENT:
            comments = Comment.objects.filter(status=Comment.STATUS_NORMAL)
            print("comments: %s" % comments)
            context = {'comments': comments}
            result = render_to_string('config_app/sidebar_comments_list.html', context=context)
        return result

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"