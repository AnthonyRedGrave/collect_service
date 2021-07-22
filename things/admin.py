from django.contrib import admin
from .models import Thing, ThingMessage, Section


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'owner', 'state', 'section', 'is_sold', 'date_published', 'deleted')
    list_display_links = ('title', 'content', 'owner', 'state')


@admin.register(ThingMessage)
class ThingMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'thing', 'deleted')
    list_display_links = ('user', 'content', 'thing')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'deleted')