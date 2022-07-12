from django.contrib import admin

from chat.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'sender', 'recipient', 'is_read', 'created', 'truncated_subject', 'truncated_content')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'sender', 'recipient')
    search_fields = (
        'subject',
        'content',
        'sender__username',
        'sender__email',
        'recipient__username',
        'recipient__email',
    )
    readonly_fields = ('created', 'modified')


admin.site.register(Message, MessageAdmin)
