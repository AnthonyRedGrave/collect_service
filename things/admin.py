from django.contrib import admin
from .models import *

@admin.action(description='CSV-Import')
def make_published(modeladmin, request, queryset):
    print(queryset)

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'owner', 'state', 'section', 'is_sold', 'date_published')
    list_display_links = ('title', 'content', 'owner', 'state')
    actions = (make_published,)

@admin.register(ThingMessage)
class ThingMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'thing')
    list_display_links = ('user', 'content', 'thing')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title',)