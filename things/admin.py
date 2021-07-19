from django.contrib import admin
from .models import *
import csv


@admin.action(description="CSV-Import")
def csv_import(modeladmin, request, queryset):
    print(queryset.model._meta.fields)

    writer = csv.writer("media/things/csv/exort.csv")


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
    actions = (csv_import,)


@admin.register(ThingMessage)
class ThingMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "thing")
    list_display_links = ("user", "content", "thing")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
