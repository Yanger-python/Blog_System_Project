from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement("context_html", item['context_html'])


class LatestPostFeed(Feed):
    feed_type = ExtendedRSSFeed
    title = "Blog system"
    link = "/rss/"
    description = "This is a blog system by django."

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse("post_detail", args=[item.pk])

    def item_context_html(self, item):
        return item.context_html

    def item_extra_kwargs(self, item):
        return {"context_html": self.item_context_html(item)}
