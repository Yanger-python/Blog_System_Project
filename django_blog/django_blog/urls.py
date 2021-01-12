"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.sitemaps import views as sitemap_views
from django_blog_app.rss import LatestPostFeed
from django_blog_app.sitemap import PostSitemap

from .custom_site import custom_site
from django_blog_app.views import post_list
from django_blog_app.views import post_detail
from django_blog_app.views import my_view, MyView, PostListView, IndexView, PostDetailView, \
    CategoryView, TagView, SearchView, AuthorView
from config.views import LinkListView
from comment.views import CommentView

urlpatterns = [
    # demo测试
    # url(r'^demo/', my_view, name="demo"),
    # url(r'^demo/', MyView.as_view(), name="demo"),
    url(r'^demo/', TemplateView.as_view(template_name="django_blog_app/post_list.html"), name="demo"),
    # 首页，或者说是所有文章列表页
    # url(r'^$', post_list, name="index"),
    url(r'^$', IndexView.as_view(), name="index"),
    # 文章详情页
    # url(r'^post/(?P<post_id>\d+).html$', post_detail, name="post_detail"),
    url(r'^post/(?P<pk>\d+).html$', PostDetailView.as_view(), name="post_detail"),
    # 文章搜索页
    url(r'^search/$', SearchView.as_view(), name="search"),
    # 作者页
    url(r'^author/(?P<owner_id>\d+)$', AuthorView.as_view(), name="author"),
    # 文章分类页
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name="category_post_list"),
    # 文章标签页
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name="tag_post_list"),
    # 文章友链
    url(r'^links/$', LinkListView.as_view(), name="links"),
    # 文章评论提交后页面
    url(r'^comment/$', CommentView.as_view(), name="comment"),
    # 配置rss
    url(r'^rss|feed/$', LatestPostFeed(), name="rss"),
    # 配置sitemap
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {"sitemaps": {'posts': PostSitemap}}),
    url(r'^super_admin/', admin.site.urls, name="super-admin"),
    url(r'^admin/', custom_site.urls, name="custom-admin"),
]
