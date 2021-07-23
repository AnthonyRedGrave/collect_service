from django.contrib import admin
from .models import *
from django.http import HttpResponse
from .services import csv_export_service
import csv


@admin.action(description="CSV-Export")
def csv_export(modeladmin, request, queryset):
    return csv_export_service()


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
    actions = (csv_export,)


@admin.register(ThingMessage)
class ThingMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "thing")
    list_display_links = ("user", "content", "thing")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title",)