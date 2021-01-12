from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView
from django.db.models import Q, F
from django.core.cache import cache

from .models import Tag, Category, Post
from config.models import SlideBar, Link
from comment.forms import CommentForm
from comment.models import Comment

from datetime import date


# Create your views here.
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        posts_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        posts_list, category = Post.get_by_category(category_id)
    else:
        print("显示所有正常状态的文章列表")
        posts_list = Post.latest_posts()
    context = {
        'tag': tag,
        'category': category,
        'posts_list': posts_list,
        'slidebars': SlideBar.get_all(),
    }
    context.update(Category.get_nav())
    print(context)
    print(type(posts_list))
    print(posts_list)
    return render(request, 'django_blog_app/post_list.html', context=context)


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'slidebars': SlideBar.get_all()
        })
        context.update(Category.get_nav())
        return context


class IndexView(CommonViewMixin, ListView):
    # 分页的总记录数
    queryset = Post.latest_posts()
    # 每页2个数据
    paginate_by = 4
    # 同模板中的变量名保持一致
    context_object_name = "posts_list"
    # 模板名称
    template_name = 'django_blog_app/post_list_demo.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        print("category_id is %s" % category_id)
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        """重写queryset方法，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get("tag_id")
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag
        })
        return context

    def get_queryset(self):
        """重写queryset方法，根据标签过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        return queryset.filter(category_id=tag_id)


class PostListView(ListView):
    model = Post
    # 分页的总记录数
    queryset = Post.latest_posts()
    # 每页2个数据
    paginate_by = 6
    context_object_name = "posts_list"
    template_name = 'django_blog_app/post_list_demo.html'


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        context.update({
            'keyword': keyword
        })
        return context

    def get_queryset(self):
        """重写queryset方法，根据文章标题或者摘要过滤"""
        queryset = super().get_queryset()
        # 获取前台输入的keyword参数
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        """重写queryset方法，根据过滤"""
        queryset = super().get_queryset()
        # 获取url中的owner_id参数
        owner_id = self.kwargs.get("owner_id")
        return queryset.filter(owner_id=owner_id)


def post_detail(request, post_id):
    try:
        posts_detail = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        posts_detail = None
    context = {'posts_detail': posts_detail,
               }
    context.update(Category.get_nav())
    return render(request, 'django_blog_app/post_detail.html', context=context)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'django_blog_app/post_detail_demo.html'
    context_object_name = "posts_detail"
    pk = "post_id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        # 该uid是在组件中给request对象添加的一个属性
        uid = self.request.uid
        pv_key = "pv:%s:%s" % (uid, self.request.path)
        # date.today()生成访问文章当天的日期
        uv_key = "uv:%s:%s:%s" % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 1分钟有效
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(pv_key, 1, 24 * 60 * 60)  # 24小时有效
        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        if increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        if increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


def my_view(request):
    if request.method == "GET":
        return HttpResponse("http使用的是get方法请求")


# 继承View基类的view类
class MyView(View):
    def get(self, request):
        return HttpResponse("http使用的是View基类的get方法请求")









