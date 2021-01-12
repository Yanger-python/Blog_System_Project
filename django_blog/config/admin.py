from django.contrib import admin

from .models import SlideBar
from django_blog.custom_site import custom_site

# Register your models here.


@admin.register(SlideBar, site=custom_site)
class SlideBarAdmin(admin.ModelAdmin):
    list_display = ("title", "display_type", "context", "status")
    fields = ("title", "display_type", "context", "status")

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.owner = request.user
        super(SlideBarAdmin, self).save_model(request, obj, form, change)
