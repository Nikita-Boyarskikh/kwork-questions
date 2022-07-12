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
    inlines = [AnswerInline, LikeInline, AccountActionGenericInline]
    list_filter = (
        'author',
        'best_answer',
        'status',
        'country',
        'language',
    )
    list_display = ('__str__', 'status', 'price', 'truncated_en_text', 'author', 'best_answer', 'country')
    search_fields = ('en_text', 'original_text', 'author')
    list_editable = ('status',)
    readonly_fields = ('status_changed', 'created', 'modified')


admin.site.register(Question, QuestionAdmin)
