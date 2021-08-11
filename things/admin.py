from django.contrib import admin
from django.http import HttpResponse

from .models import Thing, ThingMessage, Section, Deal
from things.services.csv import csv_export

from django.contrib.contenttypes.admin import GenericTabularInline
from comments.models import Comment


class CommentInline(GenericTabularInline):
    model = Comment



@admin.action(description="CSV-Export")
def csv_export_action(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="admin_export.csv"'
    file = csv_export(response)
    return file


class TagInline(admin.TabularInline):
    model = Thing.tags.through
    extra = 3


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "owner",
        "state",
        "section",
        "is_sold",
        "date_published",
        "deleted",
    )
    list_display_links = ("title", "content", "owner", "state")
    inlines = (TagInline, CommentInline)
    exclude = ('tags',)
    actions = (csv_export_action, )


@admin.register(ThingMessage)
class ThingMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "thing", "deleted")
    list_display_links = ("user", "content", "thing")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title", "deleted")


admin.site.register(Deal)