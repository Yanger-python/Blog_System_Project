from django import template

from comment.models import Comment
from comment.forms import CommentForm


register = template.Library()


# Register a callable as an inclusion tag
@register.inclusion_tag("comment_app/block.html")
def comment_block(target):
    return {
        'target': target,
        'comment_form': CommentForm,
        'comment_list': Comment.get_by_target(target),
    }