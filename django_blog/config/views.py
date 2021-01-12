from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from django_blog_app.views import CommonViewMixin
from .models import Link


# Create your views here.
class LinkListView(CommonViewMixin, ListView):
    # 模板中要渲染的友链数据
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    # 模板中要保持一致接受的值，不清楚是咋实现模板和queryset的对接
    context_object_name = "link_list"
    template_name = 'config_app/links.html'