from django.contrib import admin
from .models import *
from tags.models import Tag


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
    )
    list_display_links = ("title", "content", "owner", "state")
    inlines = (TagInline,)
    exclude = ('tags',)


@admin.register(ThingMessage)
class ThingMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "thing")
    list_display_links = ("user", "content", "thing")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
