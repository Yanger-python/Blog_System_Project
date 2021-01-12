from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Category, Tag, Post
from .adminform import PostAdminForm
from django_blog.custom_site import custom_site


class PostInline(admin.TabularInline):
    fields = ('title', 'desc', 'status')
    extra = 1
    model = Post


class BaseOwnerAdmin(admin.ModelAdmin):
    """
        1.用來自动补充文章、分类、标签、侧边栏、友链这些 Model的 owner字段
        2.用来针对 queryset 过滤当前用户的数据
    """
    exclude = ("owner",)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.owner = request.user
        super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline]
    list_display = ('name', 'owner', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryFilter(admin.SimpleListFilter):
    """自定义过滤器"""
    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('title', 'desc', 'category', 'tag', 'owner', 'created_time')
    list_display_links = ()
    list_filter = [CategoryFilter]
    # search_fields中的项不是字符类型（包含外键字段），均会报错：Related Field got invalid lookup: icontains。
    search_fields = ('title', 'category')

    # fields = ('title', 'desc', 'owner', 'category', 'tag')

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                'title',
            ),
        }),
        ('内容', {
            'fields': ('desc', 'context'),
        }),
        ('额外信息', {
            'classes': ('wide',),
            'fields': ('category', 'tag', 'status'),
        })
    )

    # 横向对齐，字段必须是多对多的关系
    # filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    # actions_on_top = True
    # actions_on_bottom = True
    #
    # save_on_top = True

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,)))
    operator.short_description = "操作"

    def __str__(self):
        return 'category'










