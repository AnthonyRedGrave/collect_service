from django.contrib import admin
from .models import *
from django.http import HttpResponse
import csv


@admin.action(description="CSV-Export")
def csv_export(modeladmin, request, queryset):
    model = queryset.model
    opts = model._meta.fields + model._meta.many_to_many
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=";")
    field_names = [field.name for field in opts]
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


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