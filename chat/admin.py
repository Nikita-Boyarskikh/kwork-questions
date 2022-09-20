from django.contrib import admin

from chat.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'sender', 'recipient', 'is_read', 'created', 'truncated_content')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'sender', 'recipient')
    search_fields = (
        'content',
        'sender__username',
        'sender__email',
        'recipient__username',
        'recipient__email',
    )


admin.site.register(Message, MessageAdmin)
