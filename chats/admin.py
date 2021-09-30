from django.contrib import admin
from .models import Chat, Message

admin.site.register(Chat)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'chat')