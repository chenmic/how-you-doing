from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    fields = ['creation_date', 'sender', 'receiver', 'subject', 'message', 'is_read']
    list_display = ['creation_date', 'sender', 'receiver', 'subject', 'message', 'is_read']
    list_filter = ['sender', 'receiver', 'is_read']
    search_fields = ['sender', 'receiver', 'subject', 'message']


admin.site.register(Message, MessageAdmin)
