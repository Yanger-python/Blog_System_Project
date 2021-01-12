from django.contrib import admin

from .models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'status', 'created_time')
    fields = ('nickname', 'context', 'created_time')

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.owner = request.user
        super(CommentAdmin, self).save_model(request, obj, form, change)