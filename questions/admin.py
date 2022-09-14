from django.contrib import admin
from django.contrib.admin import TabularInline

from accounts.admin import AccountActionGenericInline
from answers.admin import AnswerInline
from likes.admin import LikeInline
from questions.models import Question


class QuestionInline(TabularInline):
    model = Question
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline, LikeInline, AccountActionGenericInline)
    list_filter = (
        'author',
        'best_answer',
        'status',
        'country',
        'language',
    )
    list_display = ('__str__', 'status', 'price', 'en_title', 'truncated_en_text', 'author', 'best_answer', 'country')
    search_fields = ('en_text', 'original_text', 'author')
    list_editable = ('status',)
    moderator_readonly_fields = ('en_title', 'original_title', 'en_text', 'original_text', 'price', 'author', 'best_answer', 'country', 'language')  # TODO: make it editable for admin
    readonly_fields = ('status_changed', 'created', 'modified') + moderator_readonly_fields

    # TODO: make it deletable for admin
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Question, QuestionAdmin)
