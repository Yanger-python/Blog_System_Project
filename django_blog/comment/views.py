from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    print("CommentView")
    http_method_names = ["post"]
    template_name = "comment_app/result.html"

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = self.request.POST.get("target")
        print("target is %s" % target)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False
        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target
        }
        return self.render_to_response(context)
