from django.contrib import admin
from django.contrib.admin import TabularInline

from accounts.admin import AccountActionGenericInline
from answers.models import Answer
from claims.admin import ClaimInline
from likes.admin import LikeInline


class AnswerInline(TabularInline):
    model = Answer
    extra = 0


class AnswerAdmin(admin.ModelAdmin):
    inlines = [ClaimInline, LikeInline, AccountActionGenericInline]
    list_filter = (
        'author',
        'question__country',
        'question__status',
        'question',
        'language',
    )
    list_display = (
        '__str__',
        'author',
        'truncated_en_text',
        'views',
        'created',
        'question__status',
        'question__country',
        'language',
    )
    list_select_related = ('question', 'author')
    search_fields = (
        'en_text',
        'original_text',
        'question__en_text',
        'question__original_text',
        'author__username',
        'author__email',
    )
    readonly_fields = ('created', 'modified')


admin.site.register(Answer, AnswerAdmin)
