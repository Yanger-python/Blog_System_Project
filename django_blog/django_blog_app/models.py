from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property

import mistune

# Create your models here.


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )
    name = models.CharField(max_length=50, verbose_name="分类名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    @classmethod
    def get_nav(cls):
        category = Category.objects.all()
        nav_category = []
        nor_category = []
        for cate in category:
            print('cate type is %s' % cate)
            if cate.is_nav:
                nav_category.append(cate)
            else:
                nor_category.append(cate)
        return {
            'nav_category': nav_category,
            'nor_category': nor_category
        }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "分类"


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )
    name = models.CharField(max_length=10, verbose_name="标签名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"


class Post(models.Model):
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    STATUS_EDITOR = 2
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_EDITOR, "编辑"),
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )
    # 文章：主题，摘要，正文，状态，分类，标签，作者，创建时间
    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, verbose_name="摘要")
    context = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    context_html = models.TextField(verbose_name="正文html代码", blank=True, editable=False)
    # 文章状态，因该分为：草稿，正常，删除
    status = models.PositiveIntegerField(verbose_name="文章状态", choices=STATUS_ITEMS)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="标签")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.context_html = mistune.markdown(self.context)
        super().save(*args, **kwargs)

    @staticmethod
    def get_by_tag(tag_id):
        tag = None
        try:
            tag = Tag.objects.select_related().get(id=tag_id)
        except Tag.DoesNotExist:
            print('tag_id is not exist')
            posts_list = []
        else:
            posts_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return posts_list, tag

    @staticmethod
    def get_by_category(category_id):
        category = None
        try:
            category = Category.objects.select_related().get(id=category_id)
        except Category.DoesNotExist:
            print('category_id is not exist')
            posts_list = []
        else:
            posts_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return posts_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def hot_post(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
        return queryset

    # 该方法的目的是将文章多个标签用逗号分隔显示，values_list是queryset的一个接口，返回值为list类型，
    # 如果只返回模型的一个字段，需设置flat=True
    # @cached_property
    # def tags(self):
    #     return ",".join(self.tag.values_list('name', flat=True))

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]  # 根据id进行降序排列

